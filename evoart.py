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
    # HINT: 0 <= r|g|b < 256, 30 <= a <= 60, 10 <= x|y < 190
    return [(randint(0,199), randint(0,199),
             randint(0,199), randint(0,199),
             randint(0,199), randint(0,199)),
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

def evaluate(solution):
    image = draw(solution)
    diff = ImageChops.difference(image, TARGET)
    hist = diff.convert("L").histogram()
    count = sum(i * n for i, n in enumerate(hist))
    return (MAX - count) / MAX + 0.03 * (SHAPES - len(solution)) / SHAPES


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



##
# Get the best parts of both
def combine(mom, dad):
    mid = len(mom) // 2
    child = mom[:mid] + dad[mid:]
    return child

'''
    child = []

    for m_poly, d_poly in zip(mom, dad):

        coords = []
        for m, d in zip(m_poly[0], d_poly[0]):
            coords.append((m + d) // 2)
        coords = tuple(coords)

        colors = []
        for m, d in zip(m_poly[1], d_poly[1]):
            colors.append((m + d) // 2)
        colors = tuple(colors)

        child.append((coords, colors))

    #print(child)
    return child
'''


##
def mutate(chromosome, rate):

    mutated_chromosome = []

    for polygon in chromosome:

        # Small chance to add new polygons to help get out of a minor improvement loop
        if random.random() < 0.05:
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




#population = Population.generate(initialise, evaluate, size=100, maximize=True)
#draw(population[0].chromosome).save("solution.png")