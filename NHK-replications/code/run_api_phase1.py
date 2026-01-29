"""
This script samples responses from Large Language Model (LLM) APIs to generate specifications for economic research tasks.

It performs multiple runs with configurable parameters like model, temperature, and number of samples.

Outputs are saved to timestamped files in the runs directory, including metadata and the LLM's response.

Used in Phase 1 of the NHK replications project to quantify LLM choices in causal economics estimation.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
import random
from pathlib import Path
import secrets
import concurrent.futures
import time

from dotenv import load_dotenv

from llm_client import LLMClient
from path_utils import resolve_path


def build_run_id() -> str:
    # Generate a unique run ID for each specification generation attempt
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    # Combine a UTC timestamp with a short random token to avoid collisions
    return f"run_{timestamp}_{secrets.token_hex(3)}"


def load_prompt() -> str:
    # Load the prompt text from the PROMPT_JSON.md file
    prompt_path = resolve_path("PROMPT_JSON.md")
    return prompt_path.read_text(encoding="utf-8")


def write_run_output(
    output_path: Path,
    run_number: int,
    run_datetime: str,
    random_seed: int,
    model: str,
    temperature: float,
    usage: dict,
    content: str,
    prompt_variant: str | None = None,
) -> None:
    # Write the run output to a file, including metadata header and LLM response
    header = (
        "=" * 80
        + "\nRUN METADATA\n"
        + "=" * 80
        + "\n"
        + f"run_number: {run_number}\n"
        + f"datetime: {run_datetime}\n"
        + f"random_seed: {random_seed}\n"
        + f"model: {model}\n"
        + f"temperature: {temperature}\n"
        + (f"prompt_variant: {prompt_variant}\n" if prompt_variant else "")
        + f"prompt_tokens: {usage.get('prompt_tokens', '')}\n"
        + f"completion_tokens: {usage.get('completion_tokens', '')}\n"
        + f"total_tokens: {usage.get('total_tokens', '')}\n"
        + "=" * 80
        + "\nLLM RESPONSE\n"
        + "=" * 80
        + "\n"
    )
    output_path.write_text(header + content, encoding="utf-8")


def main() -> None:
    # Main function to parse arguments, set up environment, and run LLM sampling
    parser = argparse.ArgumentParser(description="Sample LLM API responses.")
    parser.add_argument("--n", type=int, required=True, help="Number of runs")
    parser.add_argument(
        "--model", type=str, default="devstral-medium-latest", help="Model name"
    )
    parser.add_argument(
        "--provider",
        type=str,
        choices=["mistral", "gemini_api"],
        default=None,
        help="LLM provider (default inferred from model)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be sent without calling API",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Optional fixed seed for reproducibility",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=2.0,
        help="Sampling temperature (mistral capped at 1.5)",
    )
    parser.add_argument(
        "--env-file",
        type=str,
        default=None,
        help="Optional path to a .env file with API keys",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=600,
        help="Total per-run timeout in seconds (default: 600)",
    )
    parser.add_argument(
        "--attempt-timeout",
        type=int,
        default=60,
        help="Per-attempt timeout in seconds (default: 60)",
    )
    parser.add_argument(
        "--retry-wait",
        type=int,
        default=2,
        help="Seconds to wait between attempts after errors/timeouts (default: 2)",
    )
    args = parser.parse_args()

    # Load environment variables from possible .env files
    env_candidates = []
    if args.env_file:
        env_candidates.append(Path(args.env_file))
    env_candidates.append(resolve_path(".env"))
    
    # Add platform-appropriate secret locations
    is_wsl = os.path.exists("/proc/version")
    try:
        is_wsl = is_wsl and "microsoft" in Path("/proc/version").read_text().lower()
    except Exception:
        is_wsl = False
    
    # Always include home directory first
    env_candidates.append(Path.home() / ".LLM-bootstrap" / "secrets.env")
    
    if is_wsl:
        # WSL mounted paths
        env_candidates.extend([
            Path("/mnt/c/Users/Brett's Workstation/.LLM-bootstrap/secrets.env"),
            Path("/mnt/c/Users/Brett/.LLM-bootstrap/secrets.env"),
        ])
    else:
        # Windows paths
        env_candidates.extend([
            Path(r"C:\Users\Brett's Workstation\.LLM-bootstrap\secrets.env"),
            Path(r"C:\Users\Brett\.LLM-bootstrap\secrets.env"),
        ])
    for env_path in env_candidates:
        if env_path.exists():
            load_dotenv(env_path)
            break

    # Determine provider if not specified
    provider = args.provider
    if provider is None:
        provider = (
            "gemini_api" if args.model.lower().startswith("gemini") else "mistral"
        )

    # Get API key based on provider
    if provider == "mistral":
        api_key = os.getenv("MISTRAL_API_KEY")
        missing_message = "MISTRAL_API_KEY not found in environment or .env"
    else:
        # Prioritize GEMINI_API_KEY, fallback to GOOGLE_API_KEY for backward compatibility
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        missing_message = "GEMINI_API_KEY not found in environment or .env"

    # Check for API key unless dry run
    if not args.dry_run and not api_key:
        raise RuntimeError(missing_message)

    # Load the prompt
    prompt = load_prompt()

    # Prepare output directory for raw run logs
    model_dir = args.model.replace("/", "_")
    runs_dir = resolve_path(f"runs/conversations/{model_dir}")
    runs_dir.mkdir(parents=True, exist_ok=True)

    # Prepare output directory for validated JSON specs (grouped by provider)
    specs_dir = resolve_path(f"specs/{provider}")
    specs_dir.mkdir(parents=True, exist_ok=True)

    # Initialize total usage tracking
    total_usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}

    # Create LLM client unless dry run
    client = None
    if not args.dry_run:
        assert api_key is not None, "API key should be set for non-dry runs"
        client = LLMClient(provider, api_key)

    # Adjust temperature if necessary for Mistral
    temperature = args.temperature
    if provider == "mistral" and temperature > 1.5:
        print(f"Requested temperature {temperature} capped at 1.5 for mistral.")
        temperature = 1.5

    # Print start message
    print(
        f"Starting {args.n} run(s) with model {args.model} via {provider} (temp={temperature})"
    )

    # Loop over the number of runs
    for i in range(1, args.n + 1):
        # Generate random seed if not provided
        random_seed = args.seed if args.seed is not None else random.randint(1, 1_000_000)

        # Get current datetime
        run_datetime = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

        # Create output file path
        output_file = runs_dir / f"run_{i}_B_{run_datetime.replace(':', '')}.txt"

        # Handle dry run
        if args.dry_run:
            print("=" * 80)
            print("DRY RUN")
            print(f"run_number: {i}")
            print(f"datetime: {run_datetime}")
            print(f"random_seed: {random_seed}")
            print(f"model: {args.model}")
            print(f"output_dir: {runs_dir}")
            print("PROMPT PREVIEW (first 500 chars):")
            print(prompt[:500])
            continue

        # Call the LLM API with a timeout
        assert client is not None  # Since dry_run would have continued earlier
        print(f"Starting run {i}...", flush=True)
        run_start = time.monotonic()
        response = None
        attempt = 0
        while True:
            attempt += 1
            elapsed = time.monotonic() - run_start
            remaining = args.timeout - elapsed
            if remaining <= 0:
                print(f"Run {i} timed out after {args.timeout}s total. Skipping.")
                break
            attempt_timeout = min(args.attempt_timeout, int(remaining))
            try:
                with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                    future = executor.submit(
                        client.complete,
                        prompt=prompt,
                        model=args.model,
                        random_seed=random_seed,
                        temperature=temperature,
                    )
                    response = future.result(timeout=attempt_timeout)
                break
            except concurrent.futures.TimeoutError:
                print(
                    f"Run {i} attempt {attempt} timed out after {attempt_timeout}s."
                )
            except Exception as exc:
                print(f"Run {i} attempt {attempt} failed with error: {exc}.")
            time.sleep(args.retry_wait)

        if response is None:
            continue

        # Attempt to parse and save a JSON spec from the response
        try:
            # Extract JSON from the response content (allowing optional ```json fences)
            content = response.content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()
            spec_data = json.loads(content)

            # Validate required fields for a spec
            required = {
                "sample_selection",
                "outcome_definition",
                "treatment_definition",
                "model_specification_line",
            }
            if not required.issubset(spec_data.keys()):
                raise ValueError(
                    f"Missing required fields: {required - set(spec_data.keys())}"
                )

            # Save the spec in the provider-specific specs directory
            run_id = build_run_id()
            spec_file = specs_dir / f"spec_{run_id}.json"
            spec_file.write_text(json.dumps(spec_data, indent=2), encoding="utf-8")
            print(f"Valid spec saved: {spec_file}")
        except (json.JSONDecodeError, ValueError) as exc:
            # If parsing fails, keep the raw response but skip spec saving
            print(f"Failed to parse/validate spec: {exc}")
            print(f"Response content: {response.content[:500]}...")

        # Write the output to file
        write_run_output(
            output_path=output_file,
            run_number=i,
            run_datetime=run_datetime,
            random_seed=random_seed,
            model=response.model,
            temperature=temperature,
            usage=response.usage,
            content=response.content,
            prompt_variant="B",
        )

        # Accumulate total usage
        for key in total_usage:
            total_usage[key] += response.usage.get(key, 0)

        # Print completion message
        print(f"Completed run {i}. Output: {output_file}")

    # Print total usage if not dry run
    if not args.dry_run:
        print("Total usage:", total_usage)


if __name__ == "__main__":
    main()
