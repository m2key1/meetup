SYSTEM_PROMPT = """
You are an expert AI specializing in efficient knowledge graph extraction from unstructured text.
"""

PROMPT = """
Your primary goal is to identify and extract relevant entities (as nodes) and their relationships (as edges) from a given text. You must output the extracted information as a single, meaningful and valid JSON object that strictly conforms to the provided schema. Only extract data that is in the provided text!

**JSON Output Schema:**

Your output must be a single JSON object with a "nodes" list and an "edges" list.

- **Node Object:** Represents an entity and must contain the following keys:
  - `id` (int): A unique, identifier (e.g., strictly increasing counter).
  - `name` (string): The primary name of the entity.
  - `type` (string): The category of the entity (e.g., 'Person', 'Organization', 'Concept').
  - `description` (string): A brief summary of the entity based ONLY on the provided text.

- **Edge Object:** Represents a directed relationship between two nodes and must contain the following keys:
  - `source_id` (int): The `id` of the source node for the relationship.
  - `target_id` (int): The `id` of the target node for the relationship.
  - `type` (string): The type of relationship (e.g., 'discovered', 'worked_at', 'located_in').
  - `description` (string): A sentence or phrase from the text that describes and justifies the relationship.

**Your Task:**

Given a user-provided text, you must perform the following steps:

1.  **Identify Entities (Nodes):**
    * Carefully read the text to identify distinct entities (people, organizations, locations, concepts, etc.).
    * For each entity, create a `Node` JSON object following the schema.
    * DO NOT REPEAT YOURSELF
    * The `id` you create is critical and must be used to link edges.

2.  **Identify Relationships (Edges):**
    * Analyze the text to find explicit relationships between the entities you have identified.
    * For each relationship, create an `Edge` JSON object. The direction matters: for "Marie Curie worked at the University of Paris," the source is Marie Curie and the target is the University of Paris.

3.  **Construct the Final JSON:**
    * Assemble all `Node` and `Edge` objects into the final `KnowledgeGraph` structure.
    * Ensure that every `source_id` and `target_id` in the `edges` list corresponds to a valid `id` in the `nodes` list.
    * Your final output must be **only the JSON object**, with no additional commentary or explanation.
    
**Example:**
**Input Text:** "Local AI provides better privacy."
**Expected JSON Output:**
```json
{{
  "nodes": [
    {{
      "id": 0,
      "name": "Local AI",
      "type": "Technology",
      "description": "AI models that run on user-owned hardware."
    }},
    {{
      "id": 1,
      "name": "Privacy",
      "type": "Benefit",
      "description": "The state of being free from unwanted observation."
    }}
  ],
  "edges": [
    {{
      "source_id": 0,
      "target_id": 1,
      "type": "provides",
      "description": "Local AI is a method that provides better privacy."
    }}
  ]
}}
```

**Constraints:**
* The output must be a single, valid JSON object and nothing else.
* If the text contains no identifiable entities or relationships, return an empty graph: `{{"nodes": [], "edges": []}}`.
* Be comprehensive. Extract ALL possible nodes and edges supported by the text. Nodes may have multiple cross connections!
* Adhere strictly to the information within the text provided.

**Real Input Text:**
{text}

**JSON Output:**
"""

OCR_PROMPT = """
Please perform OCR on this scanned document and convert it into well-structured Markdown format. 
Only return text that is actually on the document. If there is no text on the document, return nothing. DO NOT HALLUCINATE!

**Output Requirements:**
- Use proper Markdown hierarchy with headers (# ## ###) to organize content logically
- Structure lists, tables, and paragraphs appropriately 
- Maintain the original document's logical flow and organization
- Preserve formatting elements like bold, italic, and emphasis where present
- Use proper Markdown syntax for any tables, lists, or special formatting
- If the document contains handwritten text, notes, or signatures, transcribe them as accurately as possible. Clearly mark all transcribed handwritten content by enclosing it in single asterisks to render it as *italic* text. For example: *Max Mustermann*.

**Format Instructions:**
- Your response must contain ONLY the Markdown content
- Begin your response with ```
- End your response with ```
- Do not include any explanatory text, comments, or additional content outside the code block

**Structure Guidelines:**
- Create clear section headers that reflect the document's organization
- Break up long text into readable paragraphs
- Use appropriate list formatting (ordered/unordered) where applicable
- Ensure proper spacing and readability in the final Markdown output
"""