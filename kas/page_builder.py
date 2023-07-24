from fpdf import FPDF


class MakePage:
    """
    Render the page
    """
    def __init__(self, day, number, odo_start, odo_end, cover,
                 consumption, fuel_start, fuel_end, departure,
                 arriving, steps, pdf):

        self.pdf = pdf

        self.day = day
        self.number = number
        self.odo_start = odo_start
        self.odo_end = odo_end
        self.cover = cover
        self.consumption = consumption
        self.fuel_start = fuel_start
        self.fuel_end = fuel_end
        self.departure = departure
        self.arriving = arriving

        self.steps = steps

    def set_common_info(self):
        """
        Draw the general info about the day
        """
        self.pdf.set_font('Arial', 'B', 20)
        self.pdf.cell(0, 20, f'DAY: {self.day}', align='C', ln=1)

        widths = [50, 50]
        headings = ['Item', 'Value']

        # Calculate total width of the table
        total_width = sum(widths)

        # Calculate starting position to center the table
        page_width = self.pdf.w
        start_x = (page_width - total_width) / 2

        # Draw common headings info with adjusted starting position
        self.pdf.set_font('Arial', 'B', 12)
        self.pdf.set_x(start_x)

        self.pdf.set_fill_color(200, 200, 200)

        for heading, width in zip(headings, widths):

            self.pdf.cell(width, 10, heading, 1, 0, align="C", fill=True)

        self.pdf.ln()

        # initial rows to table dict
        rows_by_values = {
            0: str(self.number),
            1: str(self.odo_start),
            2: str(self.fuel_start),
            3: str(self.fuel_end),
            4: str(self.consumption),
            5: str(self.odo_end),
            6: self.departure,
            7: self.arriving
        }

        rows_by_items = {
            0: 'Path number',
            1: 'ODO at start of the day',
            2: 'Fuel at start of the day',
            3: 'Fuel at end of the day',
            4: 'Consumption per day',
            5: 'ODO at end of the day',
            6: 'Departure',
            7: 'Arriving'
        }

        self.pdf.set_fill_color(255, 255, 255)
        for item, value in zip(rows_by_items.values(),
                               rows_by_values.values()):

            self.pdf.set_x(start_x)
            self.pdf.cell(50, 10, item, 1, 0, 'C', True)
            self.pdf.cell(50, 10, value, 1, 0, 'C', True)

            self.pdf.ln()

        self.pdf.ln()

    def set_routes(self):
        """
        Draw the steps section as a table
        """
        self.pdf.set_font('helvetica', 'B', 20)
        self.pdf.cell(0, 20, 'Routes', align='C', ln=1)

        # Set font and size for the main content
        self.pdf.set_font('Arial', '', 12)

        # Create table headings
        upper_headings = ['N', 'Point to Point', 'Time', 'Total']
        lower_headings = ['/', 'Start point', 'End point', 'Hour',
                          'Min', 'Hour', 'Min', 'Km']

        # Set column widths
        upper_widths = [10, 100, 60, 20]
        lower_widths = [10, 50, 50, 15, 15, 15, 15, 20]

        # Set table header style
        self.pdf.set_fill_color(200, 200, 200)
        self.pdf.set_font('Arial', 'B', 12)

        # Draw upper headings
        for heading, width in zip(upper_headings, upper_widths):
            self.pdf.cell(width, 10, heading, 1, 0, 'C', True)

        self.pdf.ln()

        # Draw lower headings
        for heading, width in zip(lower_headings, lower_widths):
            self.pdf.cell(width, 10, heading, 1, 0, 'C', True)

        self.pdf.ln()

        # Set table data style
        self.pdf.set_fill_color(255, 255, 255)
        self.pdf.set_font('Arial', '', 10)

        # Write data in the table
        for n, ride in enumerate(self.steps):

            # initial rows to table dict
            rows = {
                0: str(n + 1),
                1: ride.get('from_AZK'),
                2: ride.get('to_AZK'),
                3: ride.get('departure').split(':')[0],
                4: ride.get('departure').split(':')[1],
                5: ride.get('arriving').split(':')[0],
                6: ride.get('arriving').split(':')[1],
                7: str(ride.get('distance'))
            }
            for num, width in enumerate(lower_widths):
                self.pdf.cell(width, 10, rows.get(num), 1, 0, 'C', True)

            self.pdf.ln()

    def set_total_distance(self):
        """
        Draw the total distance in the end of the page
        """
        self.pdf.set_font('Arial', 'I', 12)
        self.pdf.cell(0, 5, f'Total distance: {self.cover}', 1, 0, align='R')

    def build(self):
        """
        Complete the page
        """
        self.set_common_info()
        self.set_routes()
        self.set_total_distance()


def write_to_pdf(routes: list):
    """
    The function takes the prepared routes,
     and writes every day on a separate page of the PDF file
    """
    # Create an object of FPDF
    pdf = FPDF('P', 'mm', 'A4')

    # Going through the days
    for i in routes:

        # Getting data from day
        for key, value in i.items():

            # Create a new page
            pdf.add_page()

            # Create day object with current day data
            day = MakePage(
                key,
                value.get('path_number'),
                value.get('odo_at_start'),
                value.get('odo_at_end'),
                value.get('cover'),
                value.get('consumption_per_day'),
                value.get('fuel_at_start'),
                value.get('fuel_at_end'),
                value.get('departure'),
                value.get('arriving'),
                value.get('steps'),
                pdf
            )

            # Forming th page
            day.build()

    # Write to PDF
    pdf.output('output.pdf')
