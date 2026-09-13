from clean_data import CleanData
from analyze_data import RetailSalesAnalyzer

def main():
    # Clean data
    cleaner = CleanData(filepath=r"C:\Users\newik\OneDrive\Code\Python\retail_sales\retail_store_sales.csv")
    cleaner.drop_invalid_rows().fill_price_per_unit().fill_item_column().fill_discount_applied().fix_location()
    cleaner.save("cleaned_retail_data.csv")

    # Analyze
    analyzer = RetailSalesAnalyzer(df=cleaner.get_data())

    # Results
    print(analyzer.best_selling())
    print(analyzer.most_profitable())
    print(analyzer.best_selling_month())

    # Charts
    analyzer.bar_avg_revenue_per_month()
    analyzer.pie_payment_method()
    analyzer.line_sales_trending()


if __name__ == "__main__":
    main()