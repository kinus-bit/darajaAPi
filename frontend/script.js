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
    try {
      const response = await fetch("https://daraja-a-pi.vercel.app/stk_push", {
        method: "POST",
        headers: {
          "content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

	  const result = await response.json();
	  console.log("Response from backend:", result);
	  
	  // Check if there's an error in the response
	  if (result.error) {
		alert(`Error: ${result.error}`);
	  } else if (result.ResponseCode === "0") {
		alert("Payment request sent successfully! Check your phone.");
	  } else {
		alert(`Payment request sent. Response: ${result.ResponseDescription || JSON.stringify(result)}`);
	  }
	  dialog.close();
    } catch (error) {
		console.error("Error:", error);
		alert(`Failed to send payment request: ${error.message}`);
    }


 
});

//getting the access token
//DOMContentLoaded - is for ensuring the dom is fully loaded
document.addEventListener("DOMContentLoaded", async () => {
  try {
    //fetch return a promise and you use .then to resolve
    //by returning a response
	//http://127.0.0.1:8000 -for local testing
    const response = await fetch("https://daraja-a-pi.vercel.app/access", {
      method: "GET",
      headers: {
        "content-Type": "application/json",
      },
    });

	
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
   
	const data = await response.json();
	console.log("Token data:", data);
   
	const tokenContainer = document.getElementById("token");
    
    // Check if token exists
    if (data.access_token) {
      const div = document.createElement("div");
      div.innerHTML = `
        <h3>✅ Backend Connected</h3>
        <p><strong>Access Token:</strong> ${data.access_token.substring(0, 20)}...</p>
        <p><strong>Expires In:</strong> ${data.expires_in} seconds</p>
      `;
      tokenContainer.appendChild(div);
    } else if (data.error) {
      tokenContainer.innerHTML = `<p style="color: red;">❌ Error: ${data.error}</p>`;
    }
  } catch (error) {
    console.error("Error fetching token:", error.message);
    document.getElementById("token").innerHTML = `
      <p style="color: red;">❌ Cannot connect to backend: ${error.message}</p>
    `;
  }
});
