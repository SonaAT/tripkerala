function filterPlaces(input) {
    const inputValue = input.value.toLowerCase();
    const dropdown = input.nextElementSibling;
    dropdown.innerHTML = '';

    // Make a request to the Geoapify Places Autocomplete API
    const apiKey = '49503ab6c1784c298a09120883307386';
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