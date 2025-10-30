async function getConsult() {
  const concern = document.getElementById("concernInput").value;
  const responseBox = document.getElementById("responseBox");

  responseBox.innerHTML = "<div class='loading'>🩺 Generating your consultation...</div>";

  try {
    const response = await fetch("http://localhost:5000/consult", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ concern }),
    });

    const data = await response.json();

    if (data.reply) {
      const text = data.reply;

      // Split into consultation and product JSON
      const [consultText, productsJSON] = text.split("PRODUCTS_JSON:");

      const formattedConsult = consultText
        .replace("CONSULTATION:", "")
        .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
        .replace(/\*(.*?)\*/g, "<em>$1</em>")
        .replace(/\n/g, "<br>");
        

      let products = [];
      try {
        const jsonMatch = productsJSON.match(/\[([\s\S]*?)\]/);
        if (jsonMatch) products = JSON.parse(jsonMatch[0]);
      } catch (err) {
        console.error("Could not parse products JSON:", err);
      }

      // Build HTML
      let productsHTML = "";
      if (products.length > 0) {
        productsHTML = products
          .map(
            (p) => `
            <div class="product-card">
              <img src="${p.image}" alt="${p.name}" onerror="this.src='https://via.placeholder.com/150';">
              <h4>${p.name}</h4>
              <p>${p.reason}</p>
              <a href="https://www.google.com/search?q=${encodeURIComponent(
                p.name
              )}" target="_blank">🔗 View</a>
            </div>
          `
          )
          .join("");
      } else {
        productsHTML = "<p>No product recommendations found.</p>";
      }

      responseBox.innerHTML = `
        <div class="consult-box">
          <h3>🩺 Your Consultation</h3>
          <p>${formattedConsult}</p>
        </div>
        <div class="recommend-box">
          <h3>💧 Recommended Products</h3>
          <div class="product-container">${productsHTML}</div>
        </div>
      `;
    } else {
      responseBox.innerHTML = "❌ Error: " + data.error;
    }
  } catch (err) {
    responseBox.innerHTML = "⚠️ Unable to connect to server.";
  }
}
