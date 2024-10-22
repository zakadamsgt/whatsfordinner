import tkinter as tk
import time
from tkinter import simpledialog, messagebox, Scrollbar, Text
from my_functions import get_coordinates_from_address, get_weather, get_llm_response, get_user_ingredients
from PIL import Image, ImageTk

# Define global variables to store user inputs
user_lat = None
user_lng = None
weather_info = None
ingredients = None


# Function to handle address submission
def submit_address():
    global user_lat, user_lng, weather_info
    address = address_entry.get()
    if not address:
        messagebox.showerror("Input Error", "Please enter an address.")
        return

        # Run the address processing in a separate thread
        threading.Thread(target=process_address, args=(address,)).start()

    def process_address(address):
        global user_lat, user_lng, weather_info

    # Get coordinates and weather data
    try:
        user_lat, user_lng = get_coordinates_from_address(address)
        if user_lat is None or user_lng is None:
            messagebox.showerror("Error", "Unable to retrieve coordinates. Please check the address.")
            return

        temp, weather_description = get_weather(user_lat, user_lng)
        weather_info = f"{temp:.2f}°C and {weather_description}"

        #messagebox.showinfo("Weather Info", f"Weather at your location: {weather_info}")

        # Use `tkinter` methods to update the GUI #NEW
        root.after(0, lambda: messagebox.showinfo("Weather Info", f"Weather at your location: {weather_info}"))

        # Show the cuisine selection after getting the address
        root.after(0, lambda: [
            cuisine_label.grid(),
            cuisine_option.grid(),
            submit_cuisine_button.grid()
        ])

    except Exception as e:
        root.after(0, lambda: messagebox.showerror("Error", str(e)))


        # Show the cuisine selection after getting the address
        cuisine_label.grid()
        cuisine_option.grid()
        submit_cuisine_button.grid()

    except Exception as e:
        messagebox.showerror("Error", str(e))


# Function to handle cuisine submission
def submit_cuisine():
    global ingredients
    cuisine_choice = cuisine_var.get()

    if not cuisine_choice:
        messagebox.showerror("Input Error", "Please choose a cuisine type.")
        return

    # Prompt for ingredients after selecting cuisine
    ingredients = get_user_ingredients_prompt()

    if cuisine_choice == "local":
        # Example prompt for local recipe including ingredients
        local_prompt = f"Please provide a local recipe for someone in {user_lat}, {user_lng}.  Recipe selection should align with geography and what dishes are commonly served in the area and uses {ingredients}, but do not feel the need to use all the ingredients, but stick to this list. Please consider the weather as part of the recommended recipe, being {weather_info}, meaning if it's cold outside consider a warm dish and if it's warm, a light dish.  Also for the recipe selected please provide a little context on the history of the dish.  Assume the user has an intermediate level of cooking skill and feel free to provide some unique recipes.  Diversity is a key aspect of this program"
        recipe = get_llm_response(local_prompt)

        # Insert the recipe into the result_text widget
        result_text.delete(1.0, tk.END)  # Clear any previous text
        result_text.insert(tk.END, f"Suggested Local Recipe: {recipe}")

    elif cuisine_choice == "ethnic":
        # Show the ethnic type entry field
        ethnic_label.grid()
        ethnic_entry.grid()
        submit_ethnic_button.grid()


# Function to handle ethnic cuisine submission
def submit_ethnic_cuisine():
    global ingredients
    ethnic_type = ethnic_entry.get()

    if not ethnic_type:
        messagebox.showerror("Input Error", "Please enter a type of ethnic cuisine.")
        return

    # Example prompt for ethnic recipe
    ethnic_prompt = f"Please provide a {ethnic_type} recipe with {ingredients} , but do not feel the need to use all the ingredients, but stick to this list. Please consider the weather as part of the recommended recipe, being {weather_info}, meaning if it's cold outside consider a warm dish and if it's warm, a light dish. Also for the recipe selected please provide a little context on the history of the dish.  Assume the user has an intermediate level of cooking skill and feel free to provide some unique recipes.  Diversity is a key aspect of this program"
    recipe = get_llm_response(ethnic_prompt)

    # Insert the recipe into the result_text widget
    result_text.delete(1.0, tk.END)  # Clear any previous text
    result_text.insert(tk.END, f"Suggested Ethnic Recipe: {recipe}")


# Function to prompt the user for ingredients through the GUI
def get_user_ingredients_prompt():
    global ingredients
    proteins = simpledialog.askstring("Proteins",
                                      "Please list the available proteins (Chicken, Fish, Beans, etc) (Comma-separated):")
    vegetables = simpledialog.askstring("Vegetables",
                                        "Please list the available Vegetables & Fruits (Comma-separated):")
    spices = simpledialog.askstring("Spices", "Please list the available spices (Comma-separated):")

    if not proteins or not vegetables or not spices:
        messagebox.showerror("Input Error", "Please provide all the required ingredients.")
        return None

    # Store ingredients in a dictionary
    ingredients = {
        'proteins': [p.strip() for p in proteins.split(',')],
        'vegetables': [v.strip() for v in vegetables.split(',')],
        'spices': [s.strip() for s in spices.split(',')]
    }

    return ingredients


# GUI Setup
root = tk.Tk()
root.title("Recipe Generator")

# Address Entry
address_label = tk.Label(root, text="Enter your address:")
address_label.grid(row=0, column=0)

address_entry = tk.Entry(root)
address_entry.grid(row=0, column=1)

submit_address_button = tk.Button(root, text="Submit Address", command=submit_address)
submit_address_button.grid(row=0, column=2)

# Cuisine Selection
cuisine_label = tk.Label(root, text="Select Cuisine Type:")
cuisine_label.grid(row=1, column=0)
cuisine_label.grid_remove()  # Hide it initially

cuisine_var = tk.StringVar()
cuisine_option = tk.OptionMenu(root, cuisine_var, "local", "ethnic")
cuisine_option.grid(row=1, column=1)
cuisine_option.grid_remove()  # Hide it initially

submit_cuisine_button = tk.Button(root, text="Submit Cuisine Preference", command=submit_cuisine)
submit_cuisine_button.grid(row=1, column=2)
submit_cuisine_button.grid_remove()  # Hide it initially

# Ethnic Cuisine Entry
ethnic_label = tk.Label(root, text="Enter Ethnic Cuisine Type:")
ethnic_label.grid(row=2, column=0)
ethnic_label.grid_remove()  # Hide it initially

ethnic_entry = tk.Entry(root)
ethnic_entry.grid(row=2, column=1)
ethnic_entry.grid_remove()  # Hide it initially

submit_ethnic_button = tk.Button(root, text="Submit Ethnic Cuisine", command=submit_ethnic_cuisine)
submit_ethnic_button.grid(row=2, column=2)
submit_ethnic_button.grid_remove()  # Hide it initially

# Result Label with Scrollable Text Widget
result_label = tk.Label(root, text="")
result_label.grid(row=4, columnspan=3)

# Create a Text widget with scrollbar
result_text = Text(root, wrap='word', font=('Helvetica', 12), height=40)
result_text.grid(row=5, columnspan=3, sticky='nsew')

scrollbar = Scrollbar(root, command=result_text.yview)
scrollbar.grid(row=5, column=3, sticky='ns')
result_text.config(yscrollcommand=scrollbar.set)

# Start the GUI event loop
root.mainloop()
