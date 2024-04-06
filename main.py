import math
import random

input_file = "input.txt"
output_file = "output.txt"
fileout = open(output_file, "w")

A = 0                           # left limit of domain
B = 1                           # right limit of domain
a = 0                           # coefficient
b = 1                           # coefficient
c = 2                           # coefficient
precision = 0
chromosome_len = 0              # length of a chromosome
crossover_probability = 0       # (individual chromosome)
mutation_probability = 0        # (individual chromosome)
number_of_generations = 1       
number_of_chromosomes = 0       # in each generation
population = []

def get_input():
    global number_of_chromosomes
    global A, B, a, b, c
    global precision
    global crossover_probability
    global mutation_probability
    global number_of_generations
    global input_file

    file = open(input_file, "r")

    number_of_chromosomes = int(file.readline()) 
    domain = [int(x) for x in file.readline().split(" ")]
    A = domain[0]
    B = domain[1]
    coefficients = [int(x) for x in file.readline().split(" ")]
    a = coefficients[0]
    b = coefficients[1]
    c = coefficients[2]
    precision = int(file.readline())
    crossover_probability = float(file.readline())
    mutation_probability = float(file.readline())
    number_of_generations = int(file.readline())

    file.close()

def create_1st_generation():
    global chromosome_len
    global number_of_chromosomes
    global population

    #   This function will generate
    # random lists that contain 0s and 1s.

    for _ in range(number_of_chromosomes):
        chromosome = [random.randrange(2) for _ in range(chromosome_len)]
        population.append(chromosome)

def f(chromosome):
    global chromosome_len
    global a, b, c, A, B

    #   According to the course's
    # formula, that function will 
    # calculate f(x).

    power = 1
    sum = 0

    # First of all we will transform x from base 2 to base 10.
    for i in range(chromosome_len - 1, -1, -1):
        sum += chromosome[i] * power
        power *= 2

    # Course's formula.
    x = sum * (B - A) / (2 ** chromosome_len) + A

    # That will return the value of the function.
    return x * x * a + x * b + c

# Basic O(log N) binary search algorithm.

def binary_search(value, intervals):
    found = False
    left = 0
    right = len(intervals) - 1
    while found == False:
        mid = (left + right) // 2
        if intervals[mid][1][0] <= value and value <= intervals[mid][1][1]:
            return intervals[mid][0]
        elif intervals[mid][1][0] > value:
            right = mid - 1
        else:
            left = mid + 1 

# That function will generate a crossover between 2 chromosomes.

def cross2(chromosome1, chromosome2):
    global fileout
    cut = random.randint(1, len(chromosome1) - 1)
    new_chromosome1, new_chromosome2 = chromosome1[0:cut] + chromosome2[cut:], chromosome2[0:cut] + chromosome1[cut:]
    fileout.write("CROSSOVER 2 (CUT AT " + str(cut) + " - " + str(cut + 1) + ")\n")
    fileout.write(str(chromosome1) + " BECOMES " + str(new_chromosome1))
    fileout.write(str(chromosome2) + " BECOMES " + str(new_chromosome2) + "\n")
    return new_chromosome1, new_chromosome2

# That function will generate a crossover between 2 chromosomes.

def cross3(chr1, chr2, chr3):
    global fileout
    cut = random.randint(1, len(chr1) - 1)
    new_chr1, new_chr2, new_chr3 = chr1[0:cut] + chr2[cut:], chr2[0:cut] + chr3[cut:], chr3[0:cut] + chr1[cut:]
    fileout.write("CROSSOVER 3 (CUT AT " + str(cut) + " - " + str(cut + 1) + ")\n")
    fileout.write(str(chr1) + " BECOMES " + str(new_chr1))
    fileout.write(str(chr2) + " BECOMES " + str(new_chr2))
    fileout.write(str(chr3) + " BECOMES " + str(new_chr3) + "\n")
    return new_chr1, new_chr2, new_chr3

#   For the both cross functions, the "cut"
# variable means how many genes do we leave to 
# the chromosomes.

#   The next function will shuffle the chromosomes,
# and then will cross chromosomes 0 and 1, 2 and 3, etc.
# If the chromosome variable is odd, we will leave the last 
# 3 chromosome for a separate crossover.

def crossover(chromosomes):
    new_chromosomes = []
    random.shuffle(chromosomes)
    if len(chromosomes) < 2:
        return chromosomes
    if len(chromosomes) % 2 == 0:
        for i in range (0,len(chromosomes) - 1, 2):
            c1, c2 = cross2(chromosomes[i], chromosomes[i + 1])
            new_chromosomes.append(c1)
            new_chromosomes.append(c2)
    else:
        
        for i in range (0, len(chromosomes) - 4, 2):
            c1, c2 = cross2(chromosomes[i], chromosomes[i + 1])
            new_chromosomes.append(c1)
            new_chromosomes.append(c2)
        c1, c2, c3 = cross3(chromosomes[-1], chromosomes[-2], chromosomes[-3])
        new_chromosomes.append(c1)
        new_chromosomes.append(c2)
        new_chromosomes.append(c3)
    return new_chromosomes

def mutation(chromosomes):
    global mutation_probability

    #   For each chromosome we will generate 
    # a random number between 0 and 1. If that
    # number is smaller than probability of 
    # mutation, that means a random gene's of that
    # chromosome will change. 

    for i in range(len(chromosomes)) :
        prob = random.uniform(0, 1)
        if prob < mutation_probability:
            index = random.randint(0, len(chromosomes[0]) - 1)
            if chromosomes[i][index] == 0:
                chromosomes[i][index] = 1
            else:
                chromosomes[i][index] = 0
    return chromosomes

def next_generation(cnt):
    global number_of_chromosomes
    global population
    global crossover_probability
    global mutation_probability
    global fileout

    #   That function will take the current
    # population and will generate the next one.

    fileout.write("\n\n========================= GEN " + str(cnt) + " =========================")
    fileout.write("\n\nACTUAL POPULATION : \n")
    for chr in population:
        fileout.write(str(chr))
    fileout.write("\n\n")

    new_population = []             # that variable will be returned
    f_list = []                     # the list of f(x)  
    selection_p = []                # [the original position in population, [left_limit, right_limit]]
    not_selected = []               

    f_of_all_chromosomes = 0        # the sum of f(x)
    elite_chromosome_index = -1     
    elite_chromosome_power = -1     # biggest f(x)
    
    # calculate the elite chromosome

    for i in range(number_of_chromosomes):
        y = f(population[i])
        f_list.append(y)
        f_of_all_chromosomes += y
        if f_list[i] > elite_chromosome_power:
            elite_chromosome_power = f_list[i]
            elite_chromosome_index = i
    not_selected.append(population[elite_chromosome_index])

    fileout.write("F(X) FOR THIS POPULATION \n")
    fileout.write(str(f_list))

    f_list.pop(elite_chromosome_index)
    f_of_all_chromosomes -= elite_chromosome_power

    for i in range(len(f_list)):
        f_list[i] /= f_of_all_chromosomes

    # create the intervals 

    last_prob = 0
    for (i, f_) in enumerate(f_list):
        if i == number_of_chromosomes - 2:
            if i < elite_chromosome_index:
                selection_p.append([i, [last_prob, 1]])
            else:
                selection_p.append([i + 1, [last_prob, 1]])
        else:
            if i < elite_chromosome_index:
                selection_p.append([i, [last_prob, last_prob + f_list[i]]])
            else:
                selection_p.append([i + 1, [last_prob, last_prob + f_list[i]]])
            last_prob = last_prob + f_list[i]

    fileout.write("\n\nPROBABILITY OF SELECTION (EXCEPT THE ELITE CHROMOSOME) \n")
    fileout.write(str(f_list))

    fileout.write("\n\nINTERVALS : \n")
    for interval in selection_p:
        fileout.write(str(interval))

    selection_list = []
    for i in range(number_of_chromosomes - 1):
        random_number = random.uniform(0, 1)
        selection_list.append(random_number)

    picked_chromosomes = []
    crossover_values = []
    
    for (i, number) in enumerate(selection_list):
        x = binary_search(number, selection_p)
        picked_chromosomes.append(x)

    fileout.write("\n\nCHOSEN CHROMOSOMES: \n")
    fileout.write(str(picked_chromosomes))
    fileout.write("")

    # for each selected element, we will append it 
    # to old_chromosomes (if it will participate to the 
    # crossover), else to not_selected 
    old_chromosomes = []
    for i in range(len(picked_chromosomes)):
        random_number = random.uniform(0, 1)
        if random_number < crossover_probability:
            old_chromosomes.append(population[picked_chromosomes[i]])
        else:
            not_selected.append(population[picked_chromosomes[i]])

    # CROSSOVER

    new_chromosomes = crossover(old_chromosomes)

    fileout.write("\n\nCHROMOSOMES AFTER CROSSOVER:\n")
    for chr in new_chromosomes:
        fileout.write(str(chr))

    # MUTATION

    new_chromosomes = mutation(new_chromosomes)

    fileout.write("\n\nCHROMOSOMES AFTER MUTATION:\n")
    for chr in new_chromosomes:
        new_population.append(chr)
        fileout.write(str(chr))
    for chr in not_selected:
        new_population.append(chr)

    fileout.write("\n\n")

    for c in new_population:
        fileout.write(str(chr))

    return new_population

get_input()
chromosome_len = math.ceil(math.log2((B-A)*(10**precision)))
create_1st_generation()

population_copy = []
for chr in population:
    population_copy.append(chr)

cnt = 1
for i in range(number_of_generations - 1):
    population = next_generation(cnt)
    cnt += 1

start_average = 0
end_average = 0
sum_start = 0
sum_end = 0

fileout.write("\n\nFIRST POPULATION : ")
for chr in population_copy:
    fileout.write("\n\n" + str(chr) + " with value " + str(f(chr)))
    sum_start += f(chr)

fileout.write("\n\nFINAL POPULATION : ")
for chr in population:
    fileout.write("\n\n" + str(chr) + " with value " + str(f(chr)))
    sum_end += f(chr)

fileout.write("\n\nInitial Avg = " + str(sum_start / number_of_chromosomes) + " -> Final Avg = " + str(sum_end / number_of_chromosomes))
