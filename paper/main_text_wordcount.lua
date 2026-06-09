-- Count words in the manuscript body, starting at the first section header.
-- This keeps the title-page count focused on the main text rather than the
-- title block, abstract, or front-matter notes.

local function count_words_in_inlines(inlines)
  local total = 0

  for _, inline in ipairs(inlines) do
    if inline.t == "Str" then
      for _ in inline.text:gmatch("%S+") do
        total = total + 1
      end
    elseif inline.t == "Code" or inline.t == "Math" or inline.t == "Note" then
      -- Skip code, math, and footnotes so the count reflects running prose.
    elseif inline.content then
      total = total + count_words_in_inlines(inline.content)
    end
  end

  return total
end

local function block_classes(block)
  if not block.attr then
    return {}
  end

  return block.attr.classes or {}
end

local function has_class(block, target_class)
  for _, class in ipairs(block_classes(block)) do
    if class == target_class then
      return true
    end
  end

  return false
end

local function first_text_in_inlines(inlines)
  local parts = {}

  for _, inline in ipairs(inlines) do
    if inline.t == "Str" or inline.t == "Code" then
      parts[#parts + 1] = inline.text
    elseif inline.t == "Space" or inline.t == "SoftBreak" or inline.t == "LineBreak" then
      parts[#parts + 1] = " "
    elseif inline.content then
      parts[#parts + 1] = first_text_in_inlines(inline.content)
    end
  end

  return table.concat(parts)
end

local function starts_with_notes_label(block)
  if block.t ~= "Para" and block.t ~= "Plain" then
    return false
  end

  local text = first_text_in_inlines(block.content)
  text = text:gsub("^%s+", ""):lower()

  return text:match("^notes?:") ~= nil
end

local function raw_block_starts_float(block)
  if block.t ~= "RawBlock" or not block.text then
    return false
  end

  return block.text:match("\\begin%s*{%s*table%s*}") ~= nil
    or block.text:match("\\begin%s*{%s*figure%s*}") ~= nil
    or block.text:match("\\captionof%s*{%s*table%s*}") ~= nil
    or block.text:match("\\captionof%s*{%s*figure%s*}") ~= nil
end

local function is_float_block(block)
  return block.t == "Table"
    or block.t == "Figure"
    or raw_block_starts_float(block)
    or has_class(block, "table")
    or has_class(block, "figure")
end

local function count_words_in_blocks(blocks)
  local total = 0
  local previous_block_was_float = false

  for _, block in ipairs(blocks) do
    if is_float_block(block) then
      -- Tables, figures, captions, and raw LaTeX float bodies are outside main-text prose.
      previous_block_was_float = true
    elseif previous_block_was_float and starts_with_notes_label(block) then
      -- Exclude table/figure notes written as a normal paragraph immediately after a float.
      previous_block_was_float = false
    elseif block.t == "Para" or block.t == "Plain" then
      total = total + count_words_in_inlines(block.content)
      previous_block_was_float = false
    elseif block.t == "BlockQuote" or block.t == "Div" then
      total = total + count_words_in_blocks(block.content)
      previous_block_was_float = false
    elseif block.t == "BulletList" or block.t == "OrderedList" then
      for _, item in ipairs(block.content) do
        total = total + count_words_in_blocks(item)
      end
      previous_block_was_float = false
    elseif block.t == "DefinitionList" then
      for _, item in ipairs(block.content) do
        total = total + count_words_in_inlines(item[1])
        for _, definition in ipairs(item[2]) do
          total = total + count_words_in_blocks(definition)
        end
      end
      previous_block_was_float = false
    else
      previous_block_was_float = false
    end
  end

  return total
end

local function format_with_commas(value)
  local reversed = tostring(value):reverse():gsub("(%d%d%d)", "%1,")
  reversed = reversed:gsub("^,", "")
  return reversed:reverse()
end

function Pandoc(doc)
  local in_main_text = false
  local main_text_blocks = {}

  for _, block in ipairs(doc.blocks) do
    if block.t == "Header" then
      in_main_text = true
    end

    if in_main_text then
      main_text_blocks[#main_text_blocks + 1] = block
    end
  end

  local total_words = count_words_in_blocks(main_text_blocks)

  local handle = assert(io.open("LLM_replications_wordcount.tex", "w"))
  handle:write("\\newcommand{\\MainTextWordCount}{" .. format_with_commas(total_words) .. "}\n")
  handle:close()

  return doc
end
