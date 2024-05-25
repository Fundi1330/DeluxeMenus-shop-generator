from converters import OraxenForItemsConverter, VanillaForItemsConverter, OraxenForMoneyConverter, VanillaForMoneyConverter

if __name__ == '__main__':
    oraxen_items = OraxenForItemsConverter()
    oraxen_money = OraxenForMoneyConverter()
    vanilla_items = VanillaForItemsConverter()
    vanilla_money = VanillaForMoneyConverter()
    oraxen_items.convert()
    oraxen_money.convert()
    vanilla_items.convert()
    vanilla_money.convert()