from API.registration import registrationAPI, loginAPI
from API.theatre import theatreAPI, editTheatre, TheatreStatistics
from API.movie import movieAPI, MovieHome
from API.movie_timings import movie_timings, AddTimeSlot, moviefromtheatre
from API.book_tickets import book_tickets, Booking_Tickets
from API.export_csv import export_csv
from API.email import email
from API.search import search
#from API.monthly_report import MonthlyReport


def api_routes(api):
    api.add_resource(registrationAPI, "/api/registration")
    api.add_resource(loginAPI, "/api/login", "/api/user/<int:user_id>")
    api.add_resource(theatreAPI, "/api/theatre")
    api.add_resource(movieAPI, "/api/add-movie")
    api.add_resource(movie_timings, "/api/movie-timings", "/api/movie/<int:movie_id>/timings")
    api.add_resource(AddTimeSlot, "/api/add-time-slot", "/api/movie/timings/<int:slot_id>")
    api.add_resource(MovieHome, "/api/movie-home", '/api/movie/<int:movie_id>')
    api.add_resource(book_tickets, "/api/book-tickets/<int:movie_id>")
    api.add_resource(Booking_Tickets, "/api/booking", "/api/user/<int:user_id>/bookings")
    api.add_resource(editTheatre, "/api/theatre/<int:theatre_id>")
    api.add_resource(email, "/api/email")
    api.add_resource(export_csv, "/api/<int:user_id>/export-csv/<int:theatre_id>")
    api.add_resource(moviefromtheatre, "/api/moviefromtheatre/<int:theatre_id>")
    api.add_resource(search, "/api/search")
    #api.add_resource(MonthlyReport, "/api/monthly-report")
    api.add_resource(TheatreStatistics, "/api/theatre-statistics/<int:theatre_id>")