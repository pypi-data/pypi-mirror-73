from typing import Dict, List


def get_total_price_runner(groceries: List[Dict]) -> int:
    ret = get_total_price(groceries)
    print(ret)
    return ret


def get_total_price(List):
    totalGroceries = 0.0

    if type(List) is not list:
        raise Exception('The value must be a List!')

    for i in range (len(List)):
        if type(List[i]) is not dict:
            raise Exception('List value must be a dictionary')

    for i in range (len(List)):
        totalGroceries += List[i]['price']

    return totalGroceries



assert get_total_price_runner([]) == 0


assert get_total_price_runner([
	{ "product": "Milk", "quantity": 1, "price": 1.50 }
]) == 1.5

assert get_total_price_runner([
	{ "product": "Milk", "quantity": 1, "price": 1.50 },
	{ "product": "Cereals", "quantity": 1, "price": 2.50 }
]) == 4

assert get_total_price_runner([
	{ "product": "Milk", "quantity": 3, "price": 1.50 }
]) == 4.5

assert get_total_price_runner([
	{ "product": "Milk", "quantity": 1, "price": 1.50 },
	{ "product": "Eggs", "quantity": 12, "price": 0.10 },
	{ "product": "Bread", "quantity": 2, "price": 1.60 },
	{ "product": "Cheese", "quantity": 1, "price": 4.50 }
]) == 10.4

assert get_total_price_runner([
	{ "product": "Chocolate", "quantity": 1, "price": 0.10 },
	{ "product": "Lollipop", "quantity": 1, "price": 0.20 }
]) == 0.3
print("You successfully passed all Challenge 20 tests!!!")
