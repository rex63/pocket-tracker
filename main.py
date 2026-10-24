import json
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

DATA_FILE = "expenses.json"


class QuickLogApp(App):

    def build(self):
        self.title = "Pocket Tracker"
        self.records = self.load_data()

        root = BoxLayout(orientation="vertical", padding=15, spacing=10)

        # Header
        self.header = Label(
            text="Pocket Expense Tracker",
            font_size="22sp",
            size_hint_y=None,
            height=40,
            bold=True,
        )
        root.add_widget(self.header)

        # Inputs
        input_box = BoxLayout(
            orientation="horizontal", spacing=8, size_hint_y=None, height=45
        )
        self.item_input = TextInput(
            hint_text="Item name (e.g. Coffee)", multiline=False
        )
        self.cost_input = TextInput(
            hint_text="Amount (Rs)", input_filter="float", multiline=False
        )
        input_box.add_widget(self.item_input)
        input_box.add_widget(self.cost_input)
        root.add_widget(input_box)

        # Add Button
        add_btn = Button(
            text="Add Entry",
            size_hint_y=None,
            height=45,
            background_color=(0.2, 0.6, 0.86, 1),
        )
        add_btn.bind(on_press=self.add_entry)
        root.add_widget(add_btn)

        # Scrollable Display
        scroll = ScrollView(size_hint=(1, 1))
        self.display_label = Label(
            text=self.render_records(),
            size_hint_y=None,
            markup=True,
            valign="top",
            halign="left",
        )
        self.display_label.bind(
            texture_size=lambda instance, val: setattr(
                self.display_label, "height", val[1]
            )
        )
        self.display_label.bind(
            size=lambda instance, val: setattr(
                self.display_label, "text_size", (val[0], None)
            )
        )
        scroll.add_widget(self.display_label)
        root.add_widget(scroll)

        # Clear Button
        clear_btn = Button(
            text="Clear All Entries",
            size_hint_y=None,
            height=40,
            background_color=(0.85, 0.25, 0.2, 1),
        )
        clear_btn.bind(on_press=self.clear_all)
        root.add_widget(clear_btn)

        return root

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r") as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def save_data(self):
        with open(DATA_FILE, "w") as f:
            json.dump(self.records, f)

    def render_records(self):
        if not self.records:
            return "No entries yet. Add your first expense above!"
        total = sum(item["cost"] for item in self.records)
        lines = [f"[b]Total: Rs {total:.2f}[/b]\n"]
        for row in reversed(self.records):
            lines.append(f"• {row['item']}: Rs {row['cost']:.2f}")
        return "\n".join(lines)

    def add_entry(self, instance):
        name = self.item_input.text.strip()
        amt = self.cost_input.text.strip()
        if name and amt:
            self.records.append({"item": name, "cost": float(amt)})
            self.save_data()
            self.display_label.text = self.render_records()
            self.item_input.text = ""
            self.cost_input.text = ""

    def clear_all(self, instance):
        self.records = []
        self.save_data()
        self.display_label.text = self.render_records()


if __name__ == "__main__":
    QuickLogApp().run()