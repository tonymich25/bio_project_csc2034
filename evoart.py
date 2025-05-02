import random
from PIL import Image, ImageDraw
from random import randint

POLYGON_COUNT = 100
MIN_SIDES = 3
MAX_SIDES = 6
SURVIVAL = 0.1


def get_alpha():
    # Biased alpha values for polygons
    r = random.random()
    if r < 0.3:
        return randint(30, 100)
    elif r < 0.85:
        return randint(100, 200)
    else:
        return 255


def make_polygon():
    # Randomly choose a number of sides for polygon
    sides = randint(MIN_SIDES, MAX_SIDES)
    points = []

    # Assign random position for polygon
    for i in range(sides):
        points.append(randint(0, 199))
        points.append(randint(0, 199))

    colour = []
    # Assign random colour for polygon
    for i in range(3):
        colour.append(randint(0, 199))

    # Assign alpha value for polygon based on chance
    if random.random() < 0.5:
        colour.append(255)
    else:
        colour.append(get_alpha())

    return [tuple(points), tuple(colour)]


def initialise():
    return [make_polygon() for i in range(POLYGON_COUNT)]


def draw(solution):
    # Create a blank canvas with white background
    image = Image.new("RGBA", (200, 200), (255, 255, 255, 255))
    canvas = ImageDraw.Draw(image)
    # Draw each polygon on the canvas
    for polygon in solution:
        canvas.polygon(polygon[0], fill=polygon[1])
    # Return the canvas as RGB
    return image.convert("RGB")


def evolve(population, args):
    population.survive(fraction=SURVIVAL)
    population.breed(parent_picker=fit_selection, combiner=combine)
    population.mutate(mutate_function=mutate)
    return population


def fit_selection(population):
    # Select 10 random parents
    ten_parents = random.sample(population, 10)
    # Sort based on fitness
    ten_parents.sort(key=lambda fit_filter: fit_filter.fitness)
    # Return the 2 best parents
    return ten_parents[8], ten_parents[9]



def combine(mom, dad):
    # Multi-point crossover
    splits = sorted(random.sample(range(min(len(mom), len(dad))), 2))
    return mom[:splits[0]] + dad[splits[0]:splits[1]] + mom[splits[1]:]


def mutate(chromosome):
    # 50% to mutate coordinates of a polygon inside the provided chromosome
    if random.random() < 0.9:
        index = random.randrange(len(chromosome))
        coords, color = chromosome[index]
        chromosome[index] = (
            tuple(
                max(0, min(199, c + int(random.gauss(0, 10))))
                for c in coords
            ),
            color
        )

    # 50% to mutate colour of a polygon inside the provided chromosome
    elif random.random() < 0.5:
        index = random.randrange(len(chromosome))
        coords, color = chromosome[index]
        chromosome[index] = (
            coords,
            tuple(
                max(0, min(255, c + int(random.gauss(0, 25))))
                if i < 3 else c
                for i, c in enumerate(color)
            )
        )

    # 10% to create and assign a polygon to the provided chromosome
    elif random.random() < 0.1 and len(chromosome) < POLYGON_COUNT * 1.5:
        chromosome.insert(random.randrange(len(chromosome) + 1), make_polygon())
    # 5% to delete a random polygon from the provided chromosome
    elif random.random() < 0.05 and len(chromosome) > POLYGON_COUNT // 2:
        chromosome.pop(random.randrange(len(chromosome)))

    return chromosome