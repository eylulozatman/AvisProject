function getCars() {
    const selectedPickupOfficeId = document.getElementById('odalis').value;
    const selectedDropoffOfficeId = document.getElementById('odteslim').value;
    const totalDays = calculateDifference();

    // Construct the URL with all parameters as query strings
    const queryParams = new URLSearchParams({
        office_id: selectedPickupOfficeId,
        dropoff_id: selectedDropoffOfficeId,
        total_days: totalDays
    });

    const newUrl = `/getCarsByInfo?${queryParams}`;

    window.location.href = newUrl;


}


function calculateDifference() {
    const pickupInput = document.getElementById('pickupDate');
    const dropoffInput = document.getElementById('dropoffDate');

    const pickup = new Date(pickupInput.value);
    const dropoff = new Date(dropoffInput.value);
    const differenceInTime = dropoff.getTime() - pickup.getTime();
    return differenceInTime / (1000 * 3600 * 24);
}

function setDefaultDates() {
    const today = new Date();
    const pickupInput = document.getElementById('pickupDate');
    const dropoffInput = document.getElementById('dropoffDate');

    pickupInput.valueAsDate = today;

    const twoDaysLater = new Date(today);
    twoDaysLater.setDate(today.getDate() + 2);
    dropoffInput.valueAsDate = twoDaysLater;

    pickupInput.addEventListener('change', calculateDifferenceAndChangeButton);
    dropoffInput.addEventListener('change', calculateDifferenceAndChangeButton);

    calculateDifferenceAndChangeButton();
}

function calculateDifferenceAndChangeButton() {

    differenceInDays = calculateDifference()
    changeButtonText(differenceInDays);
}

// Update button text
function changeButtonText(days) {
    const button = document.getElementById('carSearch');
    button.textContent = `Rent for ${days} days`;
}


function getOfficesByCity(selectedCity, targetDropdownId) {
    const officeDropdown = document.getElementById(targetDropdownId);

    if (!selectedCity || !officeDropdown) return;

    fetch('/getOfficesByCity', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ city_id: selectedCity })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok.');
        }
        return response.json();
    })
    .then(data => {
        officeDropdown.innerHTML = '<option value="" selected disabled>Office..</option>';
        data.forEach(office => {
            const option = document.createElement('option');
            option.value = office.id;
            option.textContent = office.officename;
            officeDropdown.appendChild(option);
        });
        officeDropdown.disabled = false;
    })
    .catch(error => {
        console.error('Error fetching offices:', error);
        // Handle the error, show a message, or perform any necessary actions
    });
}


function changeSlide(car, direction) {
    var carImages = car.images;
    var currentImage = document.querySelector('.car-img .slide').getAttribute('src');
    var currentIndex = carImages.indexOf(currentImage);

    if (currentIndex === -1) {
        currentIndex = 0;
    }

    currentIndex += direction;
    if (currentIndex < 0) {
        currentIndex = carImages.length - 1;
    } else if (currentIndex >= carImages.length) {
        currentIndex = 0;
    }

    document.querySelector('.car-img .slide').setAttribute('src', carImages[currentIndex]);
}

