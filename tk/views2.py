from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LoginForm, RegisterForm
from datetime import date
from django.http import HttpResponse
import folium
import requests
from django.http import JsonResponse
import json
import numpy as np
import random as rn
from numpy.random import choice as np_choice
from tk.models import Journal,JournalImage
from datetime import datetime 
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404



class AntColony(object):

    def __init__(self, distances, n_ants, n_best, n_iterations, decay, alpha=1, beta=1):
        """
        Args:
            distances (2D numpy.array): Square matrix of distances. Diagonal is assumed to be np.inf.
            n_ants (int): Number of ants running per iteration
            n_best (int): Number of best ants who deposit pheromone
            n_iteration (int): Number of iterations
            decay (float): Rate it which pheromone decays. The pheromone value is multiplied by decay, so 0.95 will lead to decay, 0.5 to much faster decay.
            alpha (int or float): exponenet on pheromone, higher alpha gives pheromone more weight. Default=1
            beta (int or float): exponent on distance, higher beta give distance more weight. Default=1

        Example:
            ant_colony = AntColony(german_distances, 100, 20, 2000, 0.95, alpha=1, beta=2)          
        """
        self.distances  = distances
        self.pheromone = np.ones(self.distances.shape) / len(distances)
        self.all_inds = range(len(distances))
        self.n_ants = n_ants
        self.n_best = n_best
        self.n_iterations = n_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta

    def run(self):
        shortest_path = None
        all_time_shortest_path = ("placeholder", np.inf)
        for i in range(self.n_iterations):
            all_paths = self.gen_all_paths()
            self.spread_pheronome(all_paths, self.n_best, shortest_path=shortest_path)
            shortest_path = min(all_paths, key=lambda x: x[1])
            #print (shortest_path)
            if shortest_path[1] < all_time_shortest_path[1]:
                all_time_shortest_path = shortest_path            
            self.pheromone = self.pheromone * self.decay            
        return all_time_shortest_path

    def spread_pheronome(self, all_paths, n_best, shortest_path):
        sorted_paths = sorted(all_paths, key=lambda x: x[1])
        for path, dist in sorted_paths[:n_best]:
            for move in path:
                self.pheromone[move] += 1.0 / self.distances[move]

    def gen_path_dist(self, path):
        total_dist = 0
        for ele in path:
            total_dist += self.distances[ele]
        return total_dist

    def gen_all_paths(self):
        all_paths = []
        for i in range(self.n_ants):
            path = self.gen_path(0)
            all_paths.append((path, self.gen_path_dist(path)))
        return all_paths

    def gen_path(self, start):
        path = []
        visited = set()
        visited.add(start)
        prev = start
        for i in range(len(self.distances) - 1):
            move = self.pick_move(self.pheromone[prev], self.distances[prev], visited)
            path.append((prev, move))
            prev = move
            visited.add(move)
        #path.append((prev, start)) # going back to where we started    
        return path

    def pick_move(self, pheromone, dist, visited):
        pheromone = np.copy(pheromone)
        pheromone[list(visited)] = 0

        row = pheromone ** self.alpha * ((1.0 / (dist + 1e-10)) ** self.beta)

        norm_row = row / row.sum()
        move = np.random.choice(self.all_inds, 1, p=norm_row)[0]
        return move




def signin(request):
    if request.method=="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Store user-specific data in session
            request.session['user_id'] = user.id
            username = username.capitalize()
            today = date.today().strftime("%Y-%m-%d")
            return redirect("welcome")
        
        else:
            return render(request, "signin/signin.html", {
                "message" : "Invalid credentials!"
            })
    else:
        return render(request, "signin/signin.html")

        
def signout(request):
    logout(request)
    # Clear user-specific data from session on logout
    request.session.clear()
    return render(request, "signin/signin.html", {
        "message" : "Logged out!"
    })


def signup(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, "signin/signup.html", {'form': form})    
   
    if request.method == 'POST':
        form = RegisterForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            # Store user-specific data in session
            request.session['user_id'] = user.id
            username = user.username.capitalize() 
            today = date.today().strftime("%Y-%m-%d")
            return render (request, "welcome/welcome.html", {
                "username": username,
                "today": today
            }) 
        else:
            return render(request, "signin/signup.html", {'form': form})


def get_coordinates(places):
    coordinates = []
    for place in places:
        placess = place[:2]
        print(placess)
        # Construct the API request URL for each place
        url = f"https://api.geoapify.com/v1/geocode/autocomplete?text={placess}&filter=countrycode:in&bias=countrycode:in&format=json&apiKey=49503ab6c1784c298a09120883307386"
        
        # Send the request to the Geocoding API
        response = requests.get(url)
        data = response.json()

        place = ', '.join(place)

        # Extract longitude and latitude values from the response
        if 'results' in data and len(data['results']) > 0:
            for i in range(len(data['results'])):
                if data['results'][i]['state']=="Kerala" and data['results'][i]['formatted']==place:
                    break
            lon = data['results'][i]['lon']
            lat = data['results'][i]['lat']
            coordinates.append({'location': [lat, lon]})
            print(data['results'][i]['formatted'])
    
    return coordinates


def get_distance_matrix(coordinates):
    url = "https://api.geoapify.com/v1/routematrix?apiKey=82edecf6aaae4fdfb3c5ddb527d7485a"
    headers = {"Content-Type": "application/json"}

    # Prepare data for the API request
    sources = [{"location": [coord['location'][1], coord['location'][0]]} for coord in coordinates]
    targets = [{"location": [coord['location'][1], coord['location'][0]]} for coord in coordinates]
    data = {
        "mode": "drive",
        "sources": sources,
        "targets": targets,
        "traffic": "approximated"
    }

    try:
        resp = requests.post(url, headers=headers, data=json.dumps(data))
        return resp.json()
    except requests.exceptions.HTTPError as e:
        return {"error": e.response.text}



def routing(request):
    if request.method == 'POST':
        if 'route_button' in request.POST:
            # Handle form submission
            places = []
            index = 0
            while f'places[{index}]' in request.POST:
                # Assuming 'places' is the name of the input field in your form
                place_string = request.POST[f'places[{index}]']
                # Split the string by commas and strip extra whitespace from each element
                place_list = [item.strip() for item in place_string.split(',')]
                places.append(place_list)
                index += 1
            
            print(places)
            # Get coordinates for each place
            coordinates = get_coordinates(places)
            print(coordinates)
        

            distance_matrix = get_distance_matrix(coordinates)
            distances = []
            for row in distance_matrix['sources_to_targets']:
                distances_row = []
                for edge in row:
                    distances_row.append(edge['distance'])
                distances.append(distances_row)

            # Convert the distances to a numpy array
            distances = np.array(distances)
            print(distances)

            # Run the Ant Colony Optimization algorithm
            ant_colony = AntColony(distances, 10, 5, 100, 0.95, alpha=1, beta=1)
            shortest_path = ant_colony.run()
            print(shortest_path)

            # Convert each sublist to a string joined by commas
            places = [', '.join(sublist) for sublist in places]
            
            optimal_route_str = ""
            if len(places)==1:
                optimal_route_str += f"{1}. {places[0]}\n"

            elif len(shortest_path[0])==1:
                for i, edge in enumerate(shortest_path[0]):
                    optimal_route_str += f"{1}. {places[edge[0]]}\n"
                    optimal_route_str += f"{2}. {places[edge[0]+1]}\n"
            else:
                for i, edge in enumerate(shortest_path[0]):
                    optimal_route_str += f"{i+1}. {places[edge[0]]}\n"
                optimal_route_str += f"{i+2}. {places[edge[1]]}\n"

            total_distance_str=str(shortest_path[1])+" m"
            print(optimal_route_str)
            print(total_distance_str)
        
            first_list = [shortest_path[0][0]]
            print(first_list)
            # Pass the formatted output to the template
            return render(request, 'routing/routing.html', {'optimal_route': optimal_route_str, 'total_distance': total_distance_str, 'coordinates':coordinates, 'names':places, 'coord_list':first_list})
    else:
        return render(request, 'routing/routing.html')


def places_coordinates(place):

    places = place[:2]
    print(places)
        # Construct the API request URL for each place
    url = f"https://api.geoapify.com/v1/geocode/autocomplete?text={places}&format=json&apiKey=49503ab6c1784c298a09120883307386"
        
        # Send the request to the Geocoding API
    response = requests.get(url)
    data = response.json()
    #print(data)

    place = ', '.join(place)
    # Extract longitude and latitude values from the response
    if 'results' in data and len(data['results']) > 0:
        for i in range(len(data['results'])):
            if data['results'][i]['state']=="Kerala" and data['results'][i]['formatted']==place:
                break
        lon = data['results'][i]['lon']
        lat = data['results'][i]['lat']
        coordinates=[lon, lat]
    print(coordinates)
    return coordinates


def get_isolineID(coordinates):
    
    url = f"https://api.geoapify.com/v1/isoline?lat={coordinates[1]}&lon={coordinates[0]}&type=distance&mode=walk&range=5000&traffic=approximated&apiKey=49503ab6c1784c298a09120883307386"
          
    response = requests.get(url)
    data=response.json()

    isoline_id=data['properties']['id']
    return isoline_id


def places(request):
    if request.method == 'POST':
        if 'places-button' in request.POST:
            input_string = request.POST.get('places[0]', '')
            # Split the input string by commas
            place= [item.strip() for item in input_string.split(',')]

            # Now place_list contains the elements as you wanted
            print(place)

            checked_categories = request.POST.getlist('categories')
            checked_categories_str = ','.join(checked_categories)
            #print(checked_categories_str)

            # Get coordinates for each place
            coordinates = places_coordinates(place)
            #print(coordinates)
            # Create a Folium map centered at Kerala, India
            '''isoline_id=get_isolineID(coordinates)
            print(isoline_id)

            url = f"https://api.geoapify.com/v2/places?categories={checked_categories_str}&filter=geometry:{isoline_id}&bias=proximity:{coordinates[0]},{coordinates[1]}&limit=20&apiKey=49503ab6c1784c298a09120883307386"
            '''
            url = f"https://api.geoapify.com/v2/places?categories={checked_categories_str}&filter=circle:{coordinates[0]},{coordinates[1]},3000&bias=proximity:{coordinates[0]},{coordinates[1]}&limit=20&apiKey=49503ab6c1784c298a09120883307386"
            response = requests.get(url)
            data = response.json()

            #print(data)

            markers_data = []
            for feature in data.get('features', []):
                name = feature.get('properties', {}).get('name', 'Unnamed Place')
                lat = feature['geometry']['coordinates'][1]
                lon = feature['geometry']['coordinates'][0]
                categories = ', '.join(feature.get('properties', {}).get('categories', []))
                address = feature.get('properties', {}).get('formatted', 'No address available')
                marker = {'name': name, 'lat': lat, 'lon': lon, 'categories': categories, 'address': address}
                markers_data.append(marker)
            
            coord=[coordinates[1],coordinates[0]]
            print(markers_data)
            place = ', '.join(place)
            # Render the map template with the markers data
            message="Explore Further: Click on the Map to Discover Nearby Locations!"
            return render(request, 'places/places.html', {'markers_data': markers_data, 'coordinates': coord, 'place': place, 'message':message})
    else:
        return render(request, 'places/places.html')


def welcome(request):
    return render(request, 'welcome/welcome.html')

@login_required
def print_hello(request):
    # Get all journal entries for the current user
    journalData = Journal.objects.filter(user=request.user).prefetch_related('images')

    # Pass the journal entries along with the response
    return render(request, 'journal/journal.html', {'journalData': journalData})
    
@login_required
def saveJournal(request):
    if request.method == 'POST':
        jou_text = request.POST.get('journal_text')
        user = request.user  # Get the currently logged-in user
        journal_date = datetime.now().date()

        # Create the journal entry associated with the logged-in user
        journal_entry = Journal.objects.create(user=user, journal_text=jou_text, created_at=journal_date)
        
        # Handle multiple image uploads
        for i in range(1, len(request.FILES) + 1):
            if f'journal_images_{i}' in request.FILES:
                image = request.FILES[f'journal_images_{i}']
                JournalImage.objects.create(journal=journal_entry, image=image)
        
        return redirect('print_hello')
    
    return render(request, 'journal/journal.html')


