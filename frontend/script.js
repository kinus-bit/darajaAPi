let selectedPackage = null;
let selectedPrice = null;
const dialog = document.getElementById("phoneDialog");
const submitPhone = document.getElementById("payButton");

//get price according to click
const button = document.querySelectorAll(".pay-btn");

button.forEach((btn) => {
  btn.addEventListener("click", () => {
    const card = btn.closest(".package-card");
    selectedPackage = card.querySelector(".package-name").textContent;
    selectedPrice = card.querySelector(".package-price").textContent;

    console.log(selectedPackage);
    console.log(selectedPrice);
    dialog.showModal();
  });
});

submitPhone.addEventListener("click", async (e) => {
  e.preventDefault();
  const phone = document.getElementById("phoneNumber").value;
  console.log(phone);
  if (phone.length < 10) {
    alert("Enter a valid phone number!");
    return;
  }

  //prepare data
  const data = {
    phone: phone,
    price: selectedPrice,
  };

  console.log("sending to fastdaraja logic:", data);
  async () => {
    try {
      const response = await fetch("https://daraja-a-pi.vercel.app/stk_push", {
        method: "POST",
        headers: {
          "content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      const result = await response.json();
      console.log(result);
      alert("payment request sent successfully!!!");
    } catch (error) {
      console.error("error:", error.message);
    }
  };
  dialog.close();
});
