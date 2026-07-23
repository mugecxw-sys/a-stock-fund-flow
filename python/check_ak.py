import akshare as ak


print("AKShare版本:")
print(ak.__version__)


print("\n=== fund_flow相关 ===")


for name in dir(ak):

    if "fund_flow" in name.lower():

        print(name)



print("\n=== sector相关 ===")


for name in dir(ak):

    if "sector" in name.lower():

        print(name)
