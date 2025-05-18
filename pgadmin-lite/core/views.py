from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from django.http import JsonResponse
from django.apps import apps

# Utility to fetch columns of a table dynamically
def get_columns(table_name):
    with connection.cursor() as cursor:
        cursor.execute(f"""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = '{table_name}'
        """)
        columns = [row[0] for row in cursor.fetchall()]
    return columns

# Dashboard View to show all tables
def dashboard(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = [row[0] for row in cursor.fetchall()]
    return render(request, 'core/dashboard.html', {'tables': tables})

# Display records of the selected table
def table_crud(request, table_name):
    columns = get_columns(table_name)

    # Fetch all records for the table
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

    if request.method == 'POST':
        # Handle form submissions for inserting new records
        values = [request.POST.get(col) for col in columns if col != 'id']
        values_str = ', '.join(["%s"] * len(values))
        with connection.cursor() as cursor:
            cursor.execute(f"""
                INSERT INTO {table_name} ({', '.join(columns)})
                VALUES ({values_str})
            """, values)
        return redirect('table_crud', table_name=table_name)

    try:
        id_index = columns.index('id')
    except ValueError:
        id_index = None  # Handle gracefully if no 'id' column exists

    return render(request, 'core/table_crud.html', {
        'table_name': table_name,
        'columns': columns,
        'rows': rows,
        "id_index": id_index,
    })

# Update a record in the table
def update_record(request, table_name, id):
    with connection.cursor() as cursor:
        # Get column names (excluding id)
        cursor.execute(f"""
            SELECT column_name FROM information_schema.columns
            WHERE table_name = %s AND column_name != 'id'
        """, [table_name])
        columns = [row[0] for row in cursor.fetchall()]

        if request.method == 'POST':
            # Dynamically build the update query
            set_clause = ", ".join([f"{col} = %s" for col in columns])
            values = [request.POST.get(col) for col in columns]
            values.append(id)  # for the WHERE clause
            cursor.execute(
                f"UPDATE {table_name} SET {set_clause} WHERE id = %s", values
            )
            return redirect('table_crud', table_name=table_name)

        # Fetch current record values
        cursor.execute(f"SELECT id, {', '.join(columns)} FROM {table_name} WHERE id = %s", [id])
        record = cursor.fetchone()

    # Make a dict like: {'id': 16, 'title': 'X', 'author': 'Y'}
    data = dict(zip(['id'] + columns, record))
    return render(request, 'core/update_record.html', {
        'table_name': table_name,
        'columns': columns,
        'record': data
    })

# Delete a record from the table
def delete_record(request, table_name, id):
    with connection.cursor() as cursor:
        cursor.execute(f"DELETE FROM {table_name} WHERE id = %s", [id])
    return redirect('table_crud', table_name=table_name)


# View to handle running SQL queries
def run_query_view(request):
    message = None
    error = None
    columns = []
    rows = []

    if request.method == 'POST':
        query = request.POST.get('query')
        if query:
            try:
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    columns = [col[0] for col in cursor.description]
                    rows = cursor.fetchall()
                message = "Query executed successfully."
            except Exception as e:
                error = f"Error: {e}"

    return render(request, 'core/run_query.html', {
        'message': message,
        'error': error,
        'columns': columns,
        'rows': rows
    })

def query_view(request):
    result = []
    error = ""
    query = request.POST.get('query')
    if request.method == 'POST' and query:
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                if cursor.description:
                    result = cursor.fetchall()
        except Exception as e:
            error = str(e)
    return render(request, 'core/query.html', {'result': result, 'error': error})
