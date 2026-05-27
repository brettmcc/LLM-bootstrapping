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

local function count_words_in_blocks(blocks)
  local total = 0

  for _, block in ipairs(blocks) do
    if block.t == "Para" or block.t == "Plain" then
      total = total + count_words_in_inlines(block.content)
    elseif block.t == "BlockQuote" or block.t == "Div" then
      total = total + count_words_in_blocks(block.content)
    elseif block.t == "BulletList" or block.t == "OrderedList" then
      for _, item in ipairs(block.content) do
        total = total + count_words_in_blocks(item)
      end
    elseif block.t == "DefinitionList" then
      for _, item in ipairs(block.content) do
        total = total + count_words_in_inlines(item[1])
        for _, definition in ipairs(item[2]) do
          total = total + count_words_in_blocks(definition)
        end
      end
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
  local total_words = 0

  for _, block in ipairs(doc.blocks) do
    if block.t == "Header" then
      in_main_text = true
    end

    if in_main_text then
      total_words = total_words + count_words_in_blocks({ block })
    end
  end

  local handle = assert(io.open("LLM_replications_wordcount.tex", "w"))
  handle:write("\\newcommand{\\MainTextWordCount}{" .. format_with_commas(total_words) .. "}\n")
  handle:close()

  return doc
end
