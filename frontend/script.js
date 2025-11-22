let selectedPackage = null;
        let selectedPrice = 0;

        // Handle package selection
        document.querySelectorAll('.package-card').forEach(card => {
            card.addEventListener('click', function() {
                // Remove selection from all cards
                document.querySelectorAll('.package-card').forEach(c => c.classList.remove('selected'));
                
                // Add selection to clicked card
                this.classList.add('selected');
                
                // Get package details
                selectedPackage = this.dataset.package;
                selectedPrice = this.dataset.price;
                
                // Update display
                const packageInfo = document.getElementById('selectedPackage');
                const packageDisplay = document.getElementById('packageDisplay');
                packageDisplay.textContent = `${this.querySelector('.package-name').textContent} - KSH ${selectedPrice}`;
                packageInfo.style.display = 'block';
                
                // Enable pay button
                const payButton = document.getElementById('payButton');
                payButton.disabled = false;
                payButton.textContent = `Pay KSH ${selectedPrice} via M-Pesa`;
            });
        });

        // Handle form submission
        document.getElementById('paymentForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const phoneNumber = document.getElementById('phoneNumber').value;
            // const userName = document.getElementById('userName').value;
            async() =>{
                try {
                await fetch("http://0.0.0.0:8000",{
                    method:"POST",
                    body:JSON.stringify({phone_num:phoneNumber ,amount:selectedPrice })
                }).then((response)=> response.json()).then((response) =>{
                    console.log(response)
                }).catch((error) => {
                    console.error("error:",error.message)
                });

        }
                
             catch (error) {
                
                console.error("error:",error.message)
         }
           
        }
            
            // Validate phone number
            if (phoneNumber.length !== 10 || !phoneNumber.match(/^[0-9]{10}$/)) {
                showError('Please enter a valid 10-digit phone number');
                return;
            }
            
            if (!selectedPackage) {
                showError('Please select a package first');
                return;
            }
            
            // Process payment (you'll implement the actual M-Pesa API call here)
            // processPayment(phoneNumber, userName, selectedPackage, selectedPrice);
        });

        
         

        // function processPayment(phone, name, package, amount) {
        //     // Disable button during processing
        //     const payButton = document.getElementById('payButton');
        //     payButton.disabled = true;
        //     payButton.textContent = 'Processing...';
            
        //     // Simulate payment processing (replace with actual M-Pesa API call)
        //     setTimeout(() => {
        //         showSuccess();
                
        //         // Reset form after 3 seconds
        //         setTimeout(() => {
        //             document.getElementById('paymentForm').reset();
        //             document.querySelectorAll('.package-card').forEach(c => c.classList.remove('selected'));
        //             document.getElementById('selectedPackage').style.display = 'none';
        //             payButton.disabled = true;
        //             payButton.textContent = 'Select a Package to Continue';
        //             hideMessages();
        //         }, 3000);
        //     }, 2000);
            
        //     // Log payment details for your backend
        //     console.log({
        //         phone: phone,
        //         name: name,
        //         package: package,
        //         amount: amount,
        //         timestamp: new Date().toISOString()
        //     });
        // }

        function showSuccess() {
            const successMsg = document.getElementById('successMessage');
            successMsg.style.display = 'block';
            setTimeout(() => successMsg.style.display = 'none', 5000);
        }

        function showError(message) {
            const errorMsg = document.getElementById('errorMessage');
            errorMsg.textContent = '✗ ' + message;
            errorMsg.style.display = 'block';
            setTimeout(() => errorMsg.style.display = 'none', 5000);
        }

        function hideMessages() {
            document.getElementById('successMessage').style.display = 'none';
            document.getElementById('errorMessage').style.display = 'none';
        }
    