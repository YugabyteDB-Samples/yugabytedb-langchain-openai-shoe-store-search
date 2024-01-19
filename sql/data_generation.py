import random

def random_shoe_name():
    adjectives = ["Advanced", "Portable", "Ergonomic", "Efficient", "Intelligent"]
    animal = ["Gazelle", "Cheetah", "Greyhound", "Falcon"]
    nouns = ["Runner", "Sprinter", "Jogger", "Racer", "Strider", "Cloud", "Wave"]

    product_name = random.choice(adjectives) + " " + random.choice(nouns) + " " + str(random.randint(1, 10))
    return f"'{product_name}'"

PRODUCTS = {}

colors = ["'red'", "'green'", "'blue'", "'black'", "'white'", "'yellow'", "'orange'", "'purple'", "'grey'", "'pink'"]
widths = ["'narrow'", "'medium'", "'wide'"]

sql_statements = "INSERT INTO products (name, price, color, width) VALUES\n"

for i in range(1, 101):
    name = random_shoe_name()
    price = round(random.uniform(50, 150), 2)

    color1 = random.choice(colors)
    color2 = random.choice(colors)

    while(color1 == color2):
        color2 = random.choice(colors)

    width1 = random.choice(widths);
    width2 = random.choice(widths);

    while(width1 == width2):
        width2 = random.choice(widths)

    product_id = i
    PRODUCTS[product_id] = {
        "widths": [width1, width2],
        "colors": [color1, color2]
    }

    color = f"ARRAY[{color1}, {color2}]::shoe_color[]"
    width = f"ARRAY[{width1}, {width2}]::shoe_width[]"
    
    sql_statements += f"({name}, {price}, {color}, {width})"

    if i != 100:
        sql_statements += ",\n"
    else:
        sql_statements += ";"

sql_statements += "\n"

# Generate user data
users = [(f"user{i}", f"user{i}@example.com") for i in range(1, 51)]

# Generate a single SQL statement for all users
values_str = ', '.join([f"('{username}', '{email}')\n" for username, email in users])
sql_statement = f"INSERT INTO users (username, email) VALUES {values_str};"

sql_statements += sql_statement

sql_statements += "\n"

sql_statements += "INSERT INTO purchases (user_id, product_id, quantity, total_price) VALUES\n"

values_str = ""
for i in range(1, 201):
    user_id = random.randint(1,50)
    product_id = random.randint(1,100)
    quantity = 1
    total_price = round(random.uniform(50, 150), 2)

    values_str += f"({user_id}, {product_id}, {quantity}, {total_price})"

    if i != 200:
        values_str += ",\n"
    else:
        values_str += ";"

sql_statements += values_str
sql_statements += "\n"

sql_statements += "INSERT INTO product_inventory(product_id, size, color, width, quantity) VALUES"

values_str = ""
for i in range(1,101):
    product_id = i
    size = random.randint(6,15)
    color = random.choice(PRODUCTS[product_id]["colors"])
    width = random.choice(PRODUCTS[product_id]["widths"])
    quantity = random.randrange(0, 200)
    values_str += f"({product_id}, {size}, {color}, {width}, {quantity})"

    if i != 100:
        values_str += ",\n"
    else:
        values_str += ";"

sql_statements += values_str
print(sql_statements)

with open('./sql/generated_data.sql', 'w') as file:
    file.write(sql_statements)