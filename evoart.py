import random
from PIL import Image, ImageDraw
from random import randint

POLYGON_COUNT = 100
MIN_SIDES = 3
MAX_SIDES = 6
SURVIVAL = 0.1



def get_alpha():
    r = random.random()
    if r < 0.1:
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
        for i in range(sides):
            points.append(0 if random.random() < 0.5 else 199)
            points.append(0 if random.random() < 0.5 else 199)

    # Create random
    for i in range(sides):
        points.append(randint(0, 199))
        points.append(randint(0, 199))

    color=[]

    for i in range(3):
        color.append(randint(0, 199))
    if random.random() < 0.7:
        color.append(255)

    else:
        color.append(get_alpha())

    return [tuple(points), tuple(color)]


##
def initialise():
    return [make_polygon() for i in range(POLYGON_COUNT)]


##
def draw(solution):
    image = Image.new("RGBA", (200, 200), (255, 255, 255, 255))
    canvas = ImageDraw.Draw(image)

    for polygon in solution:
        canvas.polygon(polygon[0], fill=polygon[1])  # Draw each shape

    return image.convert("RGB")


def evolve(population, args):
    population.survive(fraction=SURVIVAL)
    population.breed(parent_picker=fit_selection, combiner=combine)
    population.mutate(mutate_function=mutate)
    return population


def fit_selection(population):
    ten_parents = random.sample(population, 10)
    # Sort based on fitness
    ten_parents.sort(key=lambda fit_filter: fit_filter.fitness)
    # print(ten_parents[8], ten_parents[9])
    return ten_parents[8], ten_parents[9]


## Split fit parents in half
def combine(mom, dad):
    # 70% multi-point crossover
    if random.random() < 0.7:
        splits = sorted(random.sample(range(min(len(mom), len(dad))), 2))
        return mom[:splits[0]] + dad[splits[0]:splits[1]] + mom[splits[1]:]
    # 30% uniform crossover
    else:
        return [random.choice(pair) for pair in zip(mom, dad)]


def mutate(chromosome):

    if random.random() < 0.35:
        index = random.randrange(len(chromosome))
        coords, color = chromosome[index]
        chromosome[index] = (
            tuple(
                max(0, min(199, c + int(random.gauss(0, 10))))
                for c in coords
            ),
            color
        )


    elif random.random() < 0.35:
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


    elif random.random() < 0.05 and len(chromosome) < POLYGON_COUNT * 1.5:
        chromosome.insert(random.randrange(len(chromosome) + 1), make_polygon())

    elif random.random() < 0.03 and len(chromosome) > POLYGON_COUNT // 2:
        chromosome.pop(random.randrange(len(chromosome)))

    return chromosome