import pandas as pd
import matplotlib.pyplot as plt

class RetailSalesAnalyzer:
    def __init__(self, filepath=None, df=None):
        self.data = None
        if filepath:
            self.data = pd.read_csv(filepath)
        elif df is not None:
            self.data = df.copy()
        else:
            raise ValueError('filepath or df must be provided')

    def most_profitable(self):
        """Find total revenue for items"""
        return self.data.groupby('Item')['Total Spent'].sum().sort_values(ascending=False)

    def best_selling(self):
        """Find the top 3 items by quantity sold"""
        return self.data.groupby('Item')['Quantity'].sum().nlargest(3)

    def avg_daily_sales(self):
        """Calculate average daily sales per item"""
        self.data['Transaction Date'] = pd.to_datetime(self.data['Transaction Date'])

        daily_sales = self.data.groupby(['Transaction Date', 'Item'])['Quantity'].sum()
        avg_daily_sales = daily_sales.groupby(['Item']).mean()
        return avg_daily_sales

    def best_selling_month(self):
        """Identify the best-selling month"""
        self.data['Transaction Date'] = pd.to_datetime(self.data['Transaction Date'])

        monthly = self.data.groupby(self.data['Transaction Date'].dt.to_period('M'))['Total Spent'].sum()
        return monthly.idxmax(), monthly.max()

    def bar_avg_revenue_per_month(self):
        """Show a bar chart of revenue per month"""
        self.data['Transaction Date'] = pd.to_datetime(self.data['Transaction Date'])

        # Calculate monthly revenue
        monthly_revenue = self.data.groupby(self.data['Transaction Date'].dt.month)['Total Spent'].mean()

        monthly_revenue.plot(kind='bar', color='lightblue')
        plt.title('Avg Revenue Per Month', fontsize=14)
        plt.xlabel('Month')
        plt.ylabel('Total Revenue')
        plt.xticks(rotation=0)
        return plt.show()

    def pie_payment_method(self):
        """Show a pie chart of which payment method is preferred"""
        payment_method = self.data.groupby('Location')['Payment Method'].value_counts()

        payment_method.plot(kind='pie', autopct='%1.1f%%')
        plt.title('Preferred Payment Method')
        return plt.show()

    def line_sales_trending(self):
        """Show a line chart of how are sales trending over time"""
        self.data['Transaction Date'] = pd.to_datetime(self.data['Transaction Date'])

        quarterly = self.data.groupby(self.data['Transaction Date'].dt.to_period('Q'))['Total Spent'].sum()

        quarterly.plot(kind='line', marker='o')
        plt.xlabel('Quarter / Year')
        plt.ylabel('Total Revenue')
        plt.xticks(rotation=40)
        return plt.show()