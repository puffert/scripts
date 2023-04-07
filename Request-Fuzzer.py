import requests
import re


def read_request_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    return lines


def extract_headers(lines):
    headers = {}
    for line in lines[1:]:
        if line.strip() == '':
            continue
        key, value = line.split(":", 1)
        headers[key.strip()] = value.strip()
    return headers


def find_parameters(lines, headers):
    params = []

    # Find parameters in the URL query string
    method, url, _ = lines[0].strip().split(' ')
    url_parts = url.split('?')
    if len(url_parts) > 1:
        query_string = url_parts[1]
        for param in query_string.split('&'):
            name, _ = param.split('=', 1)
            params.append(('url', name.strip()))

    # Find parameters in headers
    for key, value in headers.items():
        if key.lower() == 'cookie':
            for param in value.split(';'):
                name, _ = param.split('=', 1)
                params.append(('header', key, name.strip()))
        # Add more header checks here if needed

    return params



def fuzz_request(request_file_path):
    lines = read_request_file(request_file_path)
    headers = extract_headers(lines)
    parameters = find_parameters(lines, headers)

    if not parameters:
        print("No parameters found to fuzz.")
        return

    for i, param in enumerate(parameters, start=1):
        print(f"{i}. {param}")

    parameter_choice = int(input("Which parameter would you like to fuzz? (Enter the corresponding number): "))

    if parameter_choice < 1 or parameter_choice > len(parameters):
        print("Invalid choice.")
        return

    chosen_parameter = parameters[parameter_choice - 1]
    parameter_type = chosen_parameter[0]

    if parameter_type == 'header':
        header_name, parameter_name = chosen_parameter[1], chosen_parameter[2]
    elif parameter_type == 'url':
        parameter_name = chosen_parameter[1]

    method, original_url, _ = lines[0].strip().split(' ')
    url = original_url
    ip_address, *port_number = headers['Host'].split(':')
    port_number = port_number[0] if port_number else "443"
    schema = "https" if "https" in original_url else "http"



    fuzz_length = 0
    fuzz_step = 10
    fuzz_limit = 1000

    while fuzz_length < fuzz_limit:
        fuzz_payload = b'A' * fuzz_length

        if parameter_type == 'header':
            original_value = headers[header_name]
            headers[header_name] = headers[header_name].replace(f'{parameter_name}=', f'{parameter_name}={fuzz_payload.decode()}')
        elif parameter_type == 'url':
            url_parts = url.split('?')
            base_url, query_string = url_parts[0], url_parts[1]
            query_string = query_string.replace(f'{parameter_name}=', f'{parameter_name}={fuzz_payload.decode()}')
            url = f'{base_url}?{query_string}'

        cookie_header_length = len(headers.get('Cookie', '')) if 'Cookie' in headers else 0
        print(f"[x] Sent {len(fuzz_payload)} bytes (fuzz payload), {cookie_header_length} bytes (total Cookie header length).")

        try:
            response = requests.request(method, f'{schema}://{ip_address}:{port_number}{url}', headers=headers)

        except requests.exceptions.RequestException as e:
            print(f"[x] Server stopped responding after sending {len(fuzz_payload)} bytes.")
            break

        print(response.content.decode())
        fuzz_length += fuzz_step

        if parameter_type == 'header':
            headers[header_name] = original_value
        elif parameter_type == 'url':
            url = original_url


if __name__ == '__main__':
    request_file_path = input("Enter the path to the request file (e.g., request.txt): ")
    fuzz_request(request_file_path)
