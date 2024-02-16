# Flask_SQLAlchemy_BARTHELEMY_KYLIAN

Reservation Rooms API with flask.

# How to run project?

```console
docker compose up --build
```

# Project Parameters

## Reservation Management

### Reservation Creation

Method: _POST_

`/api/reservations`

```
{
    "id_client": 1,
    "id_chambre": 1,
    "date_arrivee": "2024-11-29",
    "date_depart": "2024-11-30"
}
```

Date format: <Year>-<Month>-<Day>

### Reservation Cancellation

Method: _DELETE_

`/api/reservations/{id}`

{id} = id of reservation

## Room Management

### Search for Available Rooms

Method: _GET_

`/api/chambres/disponibles`

```
{
    "date_arrivee": "2024-12-26",
    "date_depart": "2024-12-30"
}
```

Date format: <Year>-<Month>-<Day>

### Display all Reservations

Method: _GET_

`/api/reservations/all`

### Add a Room

Method: _POST_

`/api/chambres`

```
{
    "numero": 1,
    "type": "simple",
    "prix": "20.00",
}
```

### Modify a Room

Method: _PUT_

`/api/chambres/{id}`

{id} = id of room

### Delete a Room

Method: _DELETE_

`/api/chambres/{id}`

{id} = id of room

### Display all Rooms

Method: _GET_

`/api/chambres/all`

## Client Management

### Add a Client

Method: _POST_

`/api/clients`

```
{
    "nom": "Toto,
    "email": "t@gmail.com",
}
```

### Modify a Client

Method: _PUT_

`/api/clients/{id}`

{id} = id of client

### Delete a Client

Method: _DELETE_

`/api/clients/{id}`

{id} = id of client

### Display all Clients

Method: _GET_

`/api/clients/all`
