import flet as ft
from views.init import init_view
from views.game import game_view

def main(page: ft.Page):
    page.title = "Routes Example"
    page.theme = ft.Theme(font_family="Lexend")

    print("Initial route:", page.route)

    async def start_game(e):
        await page.push_route("/game")

    def route_change():
        print("Route change:", page.route)

        page.views.clear()
        page.views.append(
            init_view(page, on_click=start_game)
        )

        if page.route == "/game":
            page.views.append(
                game_view(page, on_click=view_pop)
            )
        page.update()

    async def view_pop():
        if page.views[-1] is not None:
            page.views.remove(page.views[-1])
            top_view = page.views[-1]
            await page.push_route(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    route_change()


if __name__ == "__main__":

    ft.run(main)