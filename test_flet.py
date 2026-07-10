import flet as ft
def main(page: ft.Page):
    print(f"main start: page.route={page.route}")
    def rc(e):
        print(f"route_change: e.route={e.route}")
        if "/scan" in page.route:
            page.route = "/"
            page.update()
            print("Set route to /")
    page.on_route_change = rc
    print(f"main end: page.route={page.route}")
    page.add(ft.Text("Hello"))
ft.app(target=main)
