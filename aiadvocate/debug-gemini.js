const { GoogleGenerativeAI } = require("@google/generative-ai");
const readline = require("readline");

// 1. API kalitni to'g'ridan-to'g'ri shu yerga yozing (Python-dagi kabi)
const API_KEY = "AIzaSyAcnhCmq5MJVL8bDgRJ7eADjDBUCsn7QEY"; 
const genAI = new GoogleGenerativeAI(API_KEY);

// 2. Modelni sozlash (Python kodingizdagi kabi 2.0-flash)
// Agarda 404 bersa, buni "gemini-1.5-flash" ga o'zgartiramiz
const model = genAI.getGenerativeModel({
  model: "gemini-2.0-flash", 
  systemInstruction: "Siz professional AI yordamchisiz. Qisqa va aniq javob bering.",
}, { apiVersion: 'v1beta' }); // Yangi modellar uchun v1beta kerak

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

async function runTest() {
  console.log("--- Node.js Gemini Test (Python analogi) ---");
  
  const ask = () => {
    rl.question("\nSiz: ", async (userInput) => {
      if (userInput.toLowerCase() === 'exit') process.exit();

      try {
        process.stdout.write("AI: ");
        
        // Python-dagi generate_content_stream kabi ishlaydi
        const result = await model.generateContentStream({
          contents: [{ role: "user", parts: [{ text: userInput }] }],
          tools: [
            { googleSearchRetrieval: {} }, // Google Search yoqish
          ],
        });

        for await (const chunk of result.stream) {
          const chunkText = chunk.text();
          process.stdout.write(chunkText);
        }
        process.stdout.write("\n");

      } catch (error) {
        console.error("\n[XATOLIK]:", error.message);
        
        if (error.message.includes("404")) {
          console.log("--- Qayta urinish: Model nomini o'zgartiraman (1.5-flash) ---");
          // Agar 2.0 topilmasa, avtomatik 1.5 ga o'tishni sinab ko'ring
        }
      }
      ask();
    });
  };

  ask();
}

runTest();