function filterPlaces(input) {
    const inputValue = input.value.toLowerCase();
    const dropdown = input.nextElementSibling;
    dropdown.innerHTML = '';

    // Make a request to the Geoapify Places Autocomplete API
    const apiKey = '82edecf6aaae4fdfb3c5ddb527d7485a';
    const apiUrl = `https://api.geoapify.com/v1/geocode/autocomplete?text=${inputValue}&filter=countrycode:in&filter=rect:75.0,8.0,78.0,13.0&apiKey=${apiKey}`;
    
    var requestOptions = {
        method: 'GET',
    };

    fetch(apiUrl, requestOptions)
        .then(response => response.json())
        .then(data => {
            // Extract suggestions from the API response
            const suggestions = data.features.map(feature => feature.properties.formatted);
            
            // Populate the dropdown with the suggestions
            suggestions.forEach(place => {
                const option = document.createElement('a');
                option.textContent = place;
                option.addEventListener('click', () => {
                    input.value = place;
                    dropdown.style.display = 'none';
                });
                dropdown.appendChild(option);
            });

            // Display the dropdown if there are suggestions
            if (suggestions.length > 0) {
                dropdown.style.display = 'block';
            } else {
                dropdown.style.display = 'none';
            }
        })
        .catch(error => {
            console.error('Error fetching places:', error);
            dropdown.style.display = 'none';
        });
}

let placeCounter = 1;
function addPlace(btn) {
    event.preventDefault();
    var placeDiv = btn.parentElement;
    var allPlaces = document.querySelectorAll('.place');
    if (placeDiv === allPlaces[allPlaces.length - 1]) {
        var newPlaceDiv = document.createElement('div');
        newPlaceDiv.classList.add('place');

        var newPlaceInput = document.createElement('input');
        newPlaceInput.setAttribute('type', 'text');
        newPlaceInput.setAttribute('name', `places[${placeCounter++}]`); // Corrected name attribute
        newPlaceInput.setAttribute('placeholder', 'Enter a place');
        newPlaceInput.setAttribute('oninput', 'filterPlaces(this)');

        var dropdownContent = document.createElement('div');
        dropdownContent.classList.add('dropdown-content');
        dropdownContent.setAttribute('id', 'dropdown-places');

        var addPlaceBtn = document.createElement('button');
        addPlaceBtn.classList.add('add-place-btn');
        addPlaceBtn.textContent = '+';
        addPlaceBtn.setAttribute('onclick', 'addPlace(this)');

        newPlaceDiv.appendChild(newPlaceInput);
        newPlaceDiv.appendChild(dropdownContent);
        newPlaceDiv.appendChild(addPlaceBtn);

        placeDiv.parentNode.insertBefore(newPlaceDiv, placeDiv.nextSibling);
    }
}


