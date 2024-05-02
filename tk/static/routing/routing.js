const places = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose", "Austin", "Jacksonville", "San Francisco", "Indianapolis", "Columbus", "Fort Worth", "Charlotte", "Seattle", "Denver", "El Paso", "Detroit", "Washington", "Boston", "Memphis", "Nashville", "Portland", "Oklahoma City", "Las Vegas", "Baltimore", "Louisville", "Milwaukee", "Albuquerque", "Tucson", "Fresno", "Sacramento", "Kansas City", "Long Beach", "Mesa", "Atlanta", "Colorado Springs", "Virginia Beach", "Raleigh", "Omaha", "Miami", "Oakland", "Minneapolis", "Tulsa", "Wichita", "New Orleans", "Arlington"];

function filterPlaces(input) {
    const inputValue = input.value.toLowerCase();
    const dropdown = input.nextElementSibling;
    dropdown.innerHTML = '';
    const filteredPlaces = places.filter(place => place.toLowerCase().includes(inputValue));
    filteredPlaces.forEach(place => {
        const option = document.createElement('a');
        option.textContent = place;
        option.addEventListener('click', () => {
            input.value = place;
            dropdown.style.display = 'none';
        });
        dropdown.appendChild(option);
    });
    if (filteredPlaces.length > 0) {
        dropdown.style.display = 'block';
    } else {
        dropdown.style.display = 'none';
    }
}

function addPlace(btn) {
    var placeDiv = btn.parentElement;
    var allPlaces = document.querySelectorAll('.place');
    if (placeDiv === allPlaces[allPlaces.length - 1]) {
        var newPlaceDiv = document.createElement('div');
        newPlaceDiv.classList.add('place');

        var newPlaceInput = document.createElement('input');
        newPlaceInput.setAttribute('type', 'text');
        newPlaceInput.setAttribute('name', 'place[]');
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
