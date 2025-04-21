import random

from evol import Population
from PIL import Image, ImageDraw, ImageChops
from random import randint

POLYGON_COUNT=100
SIDES=3
MIN_SIDES = 3
MAX_SIDES = 6
#print(SIDES)

SHAPES = 100
MAX = 255 * 200 * 200
TARGET = Image.open("8a.png")
TARGET.load()


def get_random_pixel_color():
    x = randint(0, TARGET.width - 1)
    y = randint(0, TARGET.height - 1)

    return TARGET.getpixel((x, y))

def get_alpha():
    r = random.random()
    if r < 0.3:
        return randint(30, 100)
    elif r < 0.8:
        return randint(100, 200)
    else:
        return 255

def make_polygon():
    sides = randint(MIN_SIDES, MAX_SIDES)
    points = []

    # Create shape at the edge of the canvas
    if random.random() < 0.02:
        for _ in range(sides):
            points.append(0 if random.random() < 0.5 else 199)
            points.append(0 if random.random() < 0.5 else 199)

    # Create random
    for _ in range(sides):
        points.append(randint(0, 199))
        points.append(randint(0, 199))



    if random.random() < 0.7:
        color = list(get_random_pixel_color()[:3])
        color.append(255)


    else:
        base_color = get_random_pixel_color()
        color = [max(0, min(255, base + randint(-20, 20))) for base in base_color[:3]]
        color.append(get_alpha())



    return [tuple(points), tuple(color)]

##
def initialise():
    return [make_polygon() for i in range(POLYGON_COUNT)]

##
def draw(solution):
    """Always returns RGB image for compatibility, but preserves alpha during drawing"""
    # Create RGBA canvas with white background
    image = Image.new("RGBA", (200, 200), (255, 255, 255, 255))
    canvas = ImageDraw.Draw(image)

    # Draw polygons with proper z-ordering
    for polygon in sorted(solution, key=lambda x: x[1][3] if len(x[1]) > 3 else 255):
        canvas.polygon(polygon[0], fill=polygon[1])

    # Composite onto white background and convert to RGB
    return image.convert("RGB")


def evolve(population, args):
    for i in range(5):
        population.survive(fraction=0.1)
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


def combine(mom, dad):
    # 70% multi-point crossover, 30% uniform crossover
    if random.random() < 0.7:
        splits = sorted(random.sample(range(min(len(mom), len(dad))), 2))
        return mom[:splits[0]] + dad[splits[0]:splits[1]] + mom[splits[1]:]
    else:
        return [random.choice(pair) for pair in zip(mom, dad)]



def mutate(chromosome, rate):
    # 1. Focus only on these key mutation types
    mutation_type = random.choice([
        'modify_coords',
        'modify_color',
        'add_polygon',
        'remove_polygon'
    ])

    # Work on a copy
    mutated = list(chromosome)

    # 2. Targeted coordinate mutation
    if mutation_type == 'modify_coords' and mutated:
        idx = random.randrange(len(mutated))
        coords, color = mutated[idx]
        mutated[idx] = (
            tuple(
                max(0, min(199, c + int(random.gauss(0, 10))))
                for c in coords
            ),
            color
        )

    # 3. Targeted color mutation
    elif mutation_type == 'modify_color' and mutated:
        idx = random.randrange(len(mutated))
        coords, color = mutated[idx]
        mutated[idx] = (
            coords,
            tuple(
                max(0, min(255, c + int(random.gauss(0, 25))))
                if i < 3 else c  # Don't mutate alpha
                for i, c in enumerate(color)
            )
        )

    # 4. Structural changes
    elif mutation_type == 'add_polygon' and len(mutated) < POLYGON_COUNT * 1.5:
        mutated.insert(random.randrange(len(mutated) + 1), make_polygon())

    elif mutation_type == 'remove_polygon' and len(mutated) > POLYGON_COUNT // 2:
        mutated.pop(random.randrange(len(mutated)))

    return mutated