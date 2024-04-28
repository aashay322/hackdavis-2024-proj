sys_prompt = """You will be given an image of an object. Based on the material of the object, you
must identify which of the following three categories the object fits into.

1. Recyclable (paper, glass, plastic, and aluminum)
2. Compost (food waste and other organic materials)
3. Landfill (all waste items that are not recyclable and not compostable)
4. Other (items that do not fit into the above categories)

Respond strictly with the format delimited by three backticks. Replace the sections of text
enclosed in angle brackets with your response.:
```
Recyclable: <YES or NO>
Material: <one of the above three categories>
```"""