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

  //posting data to get the prompt on the phone
  async () => {
    try {
      const response = await fetch("http://0.0.0.0:8000/stk_push", {
        method: "POST",
        headers: {
          "content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      const result = await response.json();
      console.log("data sent to backend" + result);
      alert("payment request sent successfully!!!");
    } catch (error) {
      console.error("error:", error.message);
    }
  };

  dialog.close();
});

//getting the access token
document.addEventListener("DOMContentLoaded",async () => {
    try {
		//fetch return a promise and you use .then to resolve
      await fetch("http://0.0.0.0:8000/get_token",
		{
			method: "GET",
			headers: {
			  "content-Type": "application/json",
			}
		  }
	  )
	  .then(response => response.json())
	  .then(data => console.log(data))
	  
    } catch (error) {
      console.error("error:", error.message);
    }
  });

