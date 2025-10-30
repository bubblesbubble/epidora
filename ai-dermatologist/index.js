import express from "express";
import bodyParser from "body-parser";
import dotenv from "dotenv";
import fetch from "node-fetch";
import path from "path";
import { fileURLToPath } from "url";

dotenv.config();

const app = express();
const PORT = 5000;

// Get correct __dirname in ES module
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Middleware
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, "public")));

// Gemini consultation route
app.post("/consult", async (req, res) => {
  const { concern } = req.body;

  if (!concern) {
    return res.status(400).json({ error: "Concern text is required." });
  }

  try {
    const response = await fetch(
      "https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key=" +
        process.env.GEMINI_API_KEY,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          contents: [
            {
              parts: [
                {
                  text: `
You are an expert AI dermatologist.  
For the following skin concern: "${concern}", do the following:
1️⃣ Provide a friendly, structured **consultation** explaining the condition and treatment approach.  
2️⃣ Then output a JSON array of **3 recommended skincare products** (globally available) with the following structure:
[
  {
    "name": "Product Name",
    "reason": "Why it's good for this concern",
    "image": "A realistic image URL of the product (from the brand’s site or a general product image)."
  }
]
Ensure your response is formatted like:
---
CONSULTATION:
[your detailed advice here]
---
PRODUCTS_JSON:
[your JSON here]
---
                  `,
                },
              ],
            },
          ],
        }),
      }
    );

    const data = await response.json();
    const reply =
      data?.candidates?.[0]?.content?.parts?.[0]?.text || "No response.";

    res.json({ reply });
  } catch (error) {
    console.error("Error:", error);
    res.status(500).json({ error: "Something went wrong on the server." });
  }
});

app.listen(PORT, () => console.log(`✅ Server running at http://localhost:${PORT}`))

