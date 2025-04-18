import random

from evol import Population
from PIL import Image, ImageDraw, ImageChops
from random import randint

POLYGON_COUNT=100
SIDES=3

SHAPES = 100
MAX = 255 * 200 * 200
TARGET = Image.open("8a.png")
TARGET.load()


def get_random_pixel_color():
    x = randint(0, TARGET.width - 1)
    y = randint(0, TARGET.height - 1)

    return TARGET.getpixel((x, y))

def make_polygon(n):
    if random.random() < 0.02:

        return [(0 if random.random() < 0.5 else 199, 0 if random.random() < 0.5 else 199,
                 0 if random.random() < 0.5 else 199, 0 if random.random() < 0.5 else 199,
                 0 if random.random() < 0.5 else 199, 0 if random.random() < 0.5 else 199),
                (get_random_pixel_color())]


    return [(randint(0, 199), randint(0, 199),
             randint(0, 199), randint(0, 199),
             randint(0, 199), randint(0, 199)),
            (get_random_pixel_color())]

##
def initialise():
    return [make_polygon(SIDES) for i in range(POLYGON_COUNT)]

##
def draw(solution):
    image = Image.new("RGB", (200, 200))
    canvas = ImageDraw.Draw(image, "RGBA")
    for polygon in solution:
        canvas.polygon(polygon[0], fill=polygon[1])
    return image



def evolve(population, args):
    for i in range(5):
        population.survive(fraction=0.4)
        population.breed(parent_picker=fit_selection , combiner=combine)
        population.mutate(mutate_function=mutate, rate=0.2)
    return population


##
# Original - Random Selection
def select(population):
    mom = random.choice(population)
    print(mom.fitness)

    dad = random.choice(population)
    return mom, dad


def fit_selection(population):

    ten_parents = random.sample(population, 10)
    # Sort based on fitness
    ten_parents.sort(key=lambda fit_filter: fit_filter.fitness)
    #print(ten_parents[8], ten_parents[9])
    return ten_parents[8], ten_parents[9]



## Split fit parents in half
def combine(mom, dad):
    mid = len(mom) // 2
    child = mom[:mid] + dad[mid:]
    return child



## Maybe change mutation way
def mutate(chromosome, rate):

    mutated_chromosome = []

    for polygon in chromosome:

        # Small chance to add new polygons to help get out of a minor improvement loop
        if random.random() < 0.03:
            mutated_chromosome.append(make_polygon(SIDES))

        else:
            coords = []
            for coords_poly in polygon[0]:
                coords.append(max(0, min(200, round((coords_poly + (random.random() - 0.5) * rate)))))
            coords = tuple(coords)

            colors = []
            i=0
            for colors_poly in polygon[1]:
                if i < 3:
                   colors.append(max(0, min(255, round((colors_poly + (random.random() - 0.5) * rate)))))
                else:
                    colors.append(max(30, min(60, round((colors_poly + (random.random() - 0.5) * rate)))))
            colors = tuple(colors)

            mutated_chromosome.append((coords, colors))
    return mutated_chromosome


"""def mutate(chromosome, rate, generation, current_fitness):
    mutated_chromosome = []

    # Dynamic mutation rates (aggressive early, subtle late)
    coord_rate = rate * (1.5 if generation < 20 else 0.5)  # Early: explore, Late: refine
    color_rate = rate * (1.2 if current_fitness < 0.8 else 0.3)  # Reduce color noise near plateau

    # 1. Chance to add/remove polygons (structural diversity)
    if current_fitness > 0.85 and random.random() < 0.1:
        if len(chromosome) > POLYGON_COUNT // 2 and random.random() < 0.5:
            # Remove a random polygon (simplify)
            chromosome.pop(random.randint(0, len(chromosome) - 1))
        else:
            # Add a new polygon (explore)
            chromosome.append(make_polygon(SIDES))

    # 2. Merge/Split polygons (break plateaus)
    if current_fitness > 0.85 and random.random() < 0.15:
        if random.random() < 0.5 and len(chromosome) >= 2:
            # Merge two adjacent polygons
            i = random.randint(0, len(chromosome) - 2)
            merged_coords = (
                    chromosome[i][0][:2] + chromosome[i + 1][0][2:4] + chromosome[i][0][4:]  # Mix coordinates
            )
            merged_color = tuple(
                (c1 + c2) // 2 for c1, c2 in zip(chromosome[i][1], chromosome[i + 1][1])  # Avg color
            )
            mutated_chromosome.extend(chromosome[:i] + [(merged_coords, merged_color)] + chromosome[i + 2:])
            return mutated_chromosome
        else:
            # Split a random polygon
            poly = random.choice(chromosome)
            split_idx = random.choice([2, 4])  # Split after 2nd or 4th coordinate
            new_poly1 = (poly[0][:split_idx], poly[1])
            new_poly2 = (poly[0][split_idx:], poly[1])
            mutated_chromosome.extend(chromosome + [new_poly1, new_poly2])
            return mutated_chromosome

    # 3. Standard mutations (coordinates + colors)
    for polygon in chromosome:
        # Mutate coordinates (with dynamic rate)
        new_coords = tuple(
            max(0, min(199, coord + int((random.random() - 0.5) * coord_rate)))
            for coord in polygon[0]
        )

        # Mutate color (including alpha, no hard limits)
        new_color = tuple(
            max(0, min(255, int(color + (random.random() - 0.5) * color_rate)))
            for color in polygon[1]
        )

        mutated_chromosome.append((new_coords, new_color))

    return mutated_chromosome"""



#population = Population.generate(initialise, evaluate, size=100, maximize=True)
#draw(population[0].chromosome).save("solution.png")

def debug_drawing():
    """Test if polygon drawing works correctly. Run this separately."""
    # 1. Create a test polygon covering the entire canvas
    test_poly = [(0, 0, 199, 0, 199, 199), (255, 0, 0, 60)]  # Red, opaque

    # 2. Draw it
    img = Image.new("RGB", (200, 200))
    canvas = ImageDraw.Draw(img, "RGBA")
    canvas.polygon(test_poly[0], fill=test_poly[1])

    # 3. Save and inspect
    img.save("debug_polygon.png")
    print("Saved debug_polygon.png. Check for gaps!")