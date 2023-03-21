import pandas
from fpdf import FPDF


class Product:

    def __init__(self, file_name):
        self.file_name = file_name
        self.df = pandas.read_csv(self.file_name)

    def get_product_list(self):
        return self.df


    def get_product(self, product_id):
        name = self.df.loc[self.df["id"] == int(product_id), "name"].squeeze()
        price = self.df.loc[self.df["id"] == int(product_id), "price"].squeeze()
        return name, price

    def sell(self, product_id):
        quantity = self.df.loc[self.df["id"] == int(product_id), "in stock"].squeeze()
        quantity = quantity - 1
        print(f"the new quantity is {quantity}")
        self.df.loc[self.df["id"] == product_id, "in stock"] = quantity
        self.df.to_csv(self.file_name, index=False)


class GenerateBill:
    def __init__(self, Article, price):
        self.name = Article
        self.price = price

    def to_pdf(self):
        pdf = FPDF(orientation="P", unit="mm", format="A5")
        pdf.add_page()

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Receipt nr.1", ln=1)

        pdf.cell(w=20, h=8, txt="Article: ")
        pdf.cell(w=50, h=8, txt=f"{self.name}", ln=1)

        pdf.cell(w=20, h=8, txt="Price: ")
        pdf.cell(w=50, h=8, txt=f"{self.price}", ln=1)
        pdf.output("receipt.pdf")


product = Product("articles.csv")
print(product.get_product_list())
product_id = int(input("Select the product you wanna sell> "))
product.sell(product_id)
name, price = product.get_product(product_id)
bill = GenerateBill(name, price)
bill.to_pdf()
