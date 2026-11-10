import os
from datetime import datetime

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    jsonify
)

from supabase import create_client, Client
from dotenv import load_dotenv


# -----------------------------------
# LOAD ENVIRONMENT VARIABLES
# -----------------------------------

load_dotenv()

app = Flask(__name__)

app.secret_key = os.environ.get(
    "FLASK_SECRET_KEY",
    "change-this-development-secret"
)


# -----------------------------------
# SUPABASE CONNECTION
# -----------------------------------

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError(
        "SUPABASE_URL and SUPABASE_KEY must be configured."
    )

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


# -----------------------------------
# HELPER FUNCTIONS
# -----------------------------------

def get_bus(bus_id):
    response = (
        supabase.table("bus_management")
        .select("*")
        .eq("id", bus_id)
        .eq("record_type", "BUS")
        .limit(1)
        .execute()
    )

    return response.data[0] if response.data else None


def get_bus_by_number(bus_number):
    response = (
        supabase.table("bus_management")
        .select("*")
        .eq("record_type", "BUS")
        .eq("bus_number", bus_number)
        .limit(1)
        .execute()
    )

    return response.data[0] if response.data else None


# -----------------------------------
# HOME PAGE
# -----------------------------------

@app.route("/")
def home():

    try:
        buses_response = (
            supabase.table("bus_management")
            .select("*")
            .eq("record_type", "BUS")
            .order("id", desc=True)
            .execute()
        )

        history_response = (
            supabase.table("bus_management")
            .select("*")
            .eq("record_type", "SCAN")
            .order("id", desc=True)
            .limit(100)
            .execute()
        )

        buses = buses_response.data or []
        history = history_response.data or []

        return render_template(
            "index.html",
            buses=buses,
            history=history
        )

    except Exception as e:
        app.logger.exception("Unable to load dashboard")
        flash("Unable to load bus details. Please try again.", "error")

        return render_template(
            "index.html",
            buses=[],
            history=[]
        )


# -----------------------------------
# ADD NEW BUS
# -----------------------------------

@app.route("/add_bus", methods=["POST"])
def add_bus():

    data = request.form

    bus_number = data.get("bus_number", "").strip()
    driver_name = data.get("driver_name", "").strip()
    route = data.get("route", "").strip()

    if not bus_number or not driver_name or not route:
        flash(
            "Bus number, driver name and route are required.",
            "error"
        )
        return redirect(url_for("home"))

    try:
        capacity = int(data.get("capacity") or 0)

        if capacity < 0:
            raise ValueError

    except ValueError:
        flash("Please enter a valid bus capacity.", "error")
        return redirect(url_for("home"))

    try:

        duplicate = get_bus_by_number(bus_number)

        if duplicate:
            flash("This bus number is already registered.", "error")
            return redirect(url_for("home"))

        bus_data = {
            "record_type": "BUS",
            "bus_number": bus_number,
            "registration_number": data.get(
                "registration_number", ""
            ).strip(),
            "driver_name": driver_name,
            "driver_phone": data.get(
                "driver_phone", ""
            ).strip(),
            "route": route,
            "starting_place": data.get(
                "starting_place", ""
            ).strip(),
            "stops": data.get("stops", "").strip(),
            "scheduled_arrival": data.get(
                "scheduled_arrival", ""
            ).strip(),
            "scheduled_departure": data.get(
                "scheduled_departure", ""
            ).strip(),
            "capacity": capacity,
            "event": "",
            "event_time": ""
        }

        supabase.table("bus_management").insert(
            bus_data
        ).execute()

        flash("Bus registered successfully.", "success")

    except Exception:
        app.logger.exception("Unable to add bus")
        flash("Unable to register bus. Please try again.", "error")

    return redirect(url_for("home"))


# -----------------------------------
# EDIT BUS
# -----------------------------------

@app.route("/edit_bus/<int:bus_id>", methods=["GET", "POST"])
def edit_bus(bus_id):

    try:
        bus = get_bus(bus_id)

        if bus is None:
            flash("Bus record not found.", "error")
            return redirect(url_for("home"))

        if request.method == "POST":

            data = request.form

            bus_number = data.get(
                "bus_number", ""
            ).strip()

            driver_name = data.get(
                "driver_name", ""
            ).strip()

            route = data.get("route", "").strip()

            if not bus_number or not driver_name or not route:
                flash(
                    "Bus number, driver name and route are required.",
                    "error"
                )
                return redirect(
                    url_for("edit_bus", bus_id=bus_id)
                )

            try:
                capacity = int(data.get("capacity") or 0)

                if capacity < 0:
                    raise ValueError

            except ValueError:
                flash("Please enter a valid bus capacity.", "error")
                return redirect(
                    url_for("edit_bus", bus_id=bus_id)
                )

            duplicate = get_bus_by_number(bus_number)

            if duplicate and duplicate["id"] != bus_id:
                flash(
                    "Another bus already uses this bus number.",
                    "error"
                )
                return redirect(
                    url_for("edit_bus", bus_id=bus_id)
                )

            updated_data = {
                "bus_number": bus_number,
                "registration_number": data.get(
                    "registration_number", ""
                ).strip(),
                "driver_name": driver_name,
                "driver_phone": data.get(
                    "driver_phone", ""
                ).strip(),
                "route": route,
                "starting_place": data.get(
                    "starting_place", ""
                ).strip(),
                "stops": data.get("stops", "").strip(),
                "scheduled_arrival": data.get(
                    "scheduled_arrival", ""
                ).strip(),
                "scheduled_departure": data.get(
                    "scheduled_departure", ""
                ).strip(),
                "capacity": capacity
            }

            (
                supabase.table("bus_management")
                .update(updated_data)
                .eq("id", bus_id)
                .eq("record_type", "BUS")
                .execute()
            )

            flash(
                "Bus details updated successfully.",
                "success"
            )

            return redirect(url_for("home"))

        return render_template(
            "edit_bus.html",
            bus=bus
        )

    except Exception:
        app.logger.exception("Unable to edit bus")
        flash("Unable to update bus details.", "error")
        return redirect(url_for("home"))


# -----------------------------------
# QR CODE SCANNING API
# -----------------------------------

@app.route("/api/scan", methods=["POST"])
def scan_bus():

    data = request.get_json(silent=True) or {}

    bus_number = str(
        data.get("bus_number", "")
    ).strip()

    event = str(
        data.get("event", "Arrival")
    ).strip().title()

    if not bus_number:
        return jsonify({
            "success": False,
            "message": "Bus number is required."
        }), 400

    if event not in ("Arrival", "Departure"):
        return jsonify({
            "success": False,
            "message": "Invalid event."
        }), 400

    try:

        # Find registered bus
        bus = get_bus_by_number(bus_number)

        if bus is None:
            return jsonify({
                "success": False,
                "message": "Bus is not registered."
            }), 404

        # Current scan time
        scan_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        # Save scan record in Supabase
        scan_data = {
            "record_type": "SCAN",
            "bus_number": bus["bus_number"],
            "registration_number": bus.get("registration_number"),
            "driver_name": bus.get("driver_name"),
            "driver_phone": bus.get("driver_phone"),
            "route": bus.get("route"),
            "starting_place": bus.get("starting_place"),
            "stops": bus.get("stops"),
            "scheduled_arrival": bus.get("scheduled_arrival"),
            "scheduled_departure": bus.get("scheduled_departure"),
            "capacity": bus.get("capacity"),
            "event": event,
            "event_time": scan_time
        }

        supabase.table("bus_management").insert(
            scan_data
        ).execute()

        return jsonify({
            "success": True,
            "message": (
                f"{bus_number}: {event} recorded successfully."
            ),
            "bus_number": bus_number,
            "event": event,
            "event_time": scan_time
        })

    except Exception:
        app.logger.exception("QR scan failed")

        return jsonify({
            "success": False,
            "message": "Unable to save scan details."
        }), 500


# -----------------------------------
# RUN APPLICATION
# -----------------------------------

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )