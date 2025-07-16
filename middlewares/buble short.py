import tkinter as tk
from tkinter import simpledialog, messagebox
import math
import time

# --- Kelas untuk Node ---
class Node:
    """Mendefinisikan sebuah node dalam Double Linked List."""
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

# --- Kelas untuk Circular Double Linked List ---
class CircularDoubleLinkedList:
    """Logika untuk Circular Double Linked List."""
    def __init__(self):
        self.head = None
        self.count = 0

    def insert_at_head(self, data):
        new_node = Node(data)
        self.count += 1
        if not self.head:
            self.head = new_node
            new_node.next = new_node
            new_node.prev = new_node
        else:
            last_node = self.head.prev
            new_node.next = self.head
            new_node.prev = last_node
            self.head.prev = new_node
            last_node.next = new_node
            self.head = new_node
        return new_node

    def insert_at_tail(self, data):
        if not self.head:
            return self.insert_at_head(data)
        
        new_node = Node(data)
        self.count += 1
        last_node = self.head.prev
        last_node.next = new_node
        new_node.prev = last_node
        new_node.next = self.head
        self.head.prev = new_node
        return new_node

    def delete_node(self, key):
        if not self.head:
            return None, None # Tidak ada yang dihapus

        current = self.head
        node_to_delete = None

        # Cari node yang akan dihapus
        for _ in range(self.count):
            if current.data == key:
                node_to_delete = current
                break
            current = current.next
        
        if not node_to_delete:
            return None, None # Node tidak ditemukan

        # Jika hanya ada satu node
        if self.count == 1:
            self.head = None
        else:
            prev_node = node_to_delete.prev
            next_node = node_to_delete.next
            prev_node.next = next_node
            next_node.prev = prev_node
            if node_to_delete == self.head:
                self.head = next_node
        
        self.count -= 1
        return node_to_delete, node_to_delete.prev # return node yg dihapus dan node sebelumnya

    def find_node(self, key):
        if not self.head:
            return None
        current = self.head
        for _ in range(self.count):
            if current.data == key:
                return current
            current = current.next
        return None

    def get_nodes(self):
        nodes = []
        if not self.head:
            return nodes
        current = self.head
        for _ in range(self.count):
            nodes.append(current)
            current = current.next
        return nodes

# --- Kelas Aplikasi GUI ---
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Animasi Circular Double Linked List")
        self.geometry("800x650")

        self.cdll = CircularDoubleLinkedList()
        self.node_positions = {}
        self.node_drawing = {}

        # Canvas untuk menggambar
        self.canvas = tk.Canvas(self, bg="white", width=800, height=500)
        self.canvas.pack(pady=20)

        # Frame untuk kontrol
        control_frame = tk.Frame(self)
        control_frame.pack(pady=10)

        # Tombol-tombol
        tk.Button(control_frame, text="Tambah di Awal", command=self.add_head).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Tambah di Akhir", command=self.add_tail).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Hapus Node", command=self.delete).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Cari Node", command=self.find).pack(side=tk.LEFT, padx=5)
        
        # Label Status
        self.status_label = tk.Label(self, text="Selamat Datang!", fg="blue")
        self.status_label.pack()

        self.draw_list()

    def update_status(self, message, color="blue"):
        self.status_label.config(text=message, fg=color)
        self.update_idletasks()

    def calculate_positions(self):
        self.node_positions.clear()
        nodes = self.cdll.get_nodes()
        count = len(nodes)
        if count == 0:
            return
            
        center_x, center_y = 400, 250
        radius = 180
        
        for i, node in enumerate(nodes):
            angle = (2 * math.pi / count) * i - (math.pi / 2) # Start from top
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            self.node_positions[node] = (x, y)

    def draw_list(self, highlight_node=None, color="lightblue"):
        self.canvas.delete("all")
        self.node_drawing.clear()
        self.calculate_positions()

        if not self.cdll.head:
            self.canvas.create_text(400, 250, text="Linked List Kosong", font=("Arial", 16))
            return

        # Gambar panah (pointer) terlebih dahulu
        for node, pos in self.node_positions.items():
            if node.next:
                self.draw_arrow(node, node.next, "blue", "next")
            if node.prev:
                self.draw_arrow(node, node.prev, "red", "prev")

        # Gambar node
        for node, pos in self.node_positions.items():
            self.draw_node(node, pos, highlight_node, color)
        
        # Tandai Head
        if self.cdll.head:
            head_pos = self.node_positions[self.cdll.head]
            self.canvas.create_text(head_pos[0], head_pos[1] + 45, text="HEAD", font=("Arial", 10, "bold"), fill="green")


    def draw_node(self, node, pos, highlight_node, color):
        x, y = pos
        fill_color = color if node == highlight_node else "skyblue"
        outline_color = "black"
        
        node_id = self.canvas.create_oval(x-25, y-25, x+25, y+25, fill=fill_color, outline=outline_color, width=2)
        text_id = self.canvas.create_text(x, y, text=str(node.data), font=("Arial", 12, "bold"))
        self.node_drawing[node] = (node_id, text_id)

    def draw_arrow(self, from_node, to_node, color, direction):
        if from_node not in self.node_positions or to_node not in self.node_positions:
            return

        pos1 = self.node_positions[from_node]
        pos2 = self.node_positions[to_node]

        # Calculate control points for curved line
        mid_x = (pos1[0] + pos2[0]) / 2
        mid_y = (pos1[1] + pos2[1]) / 2
        
        # Offset control point to make the line curve outwards
        offset_scale = 0.2
        ctrl_x = mid_x + offset_scale * (pos2[1] - pos1[1])
        ctrl_y = mid_y - offset_scale * (pos2[0] - pos1[0])

        # Adjust arrow start/end points to be on the edge of the circle
        angle = math.atan2(pos2[1] - pos1[1], pos2[0] - pos1[0])
        start_x = pos1[0] + 25 * math.cos(angle)
        start_y = pos1[1] + 25 * math.sin(angle)
        
        end_angle = math.atan2(pos1[1] - pos2[1], pos1[0] - pos2[0])
        end_x = pos2[0] + 25 * math.cos(end_angle)
        end_y = pos2[1] + 25 * math.sin(end_angle)
        
        # Different curve for prev pointer
        if direction == 'prev':
             ctrl_x = mid_x - offset_scale * (pos2[1] - pos1[1])
             ctrl_y = mid_y + offset_scale * (pos2[0] - pos1[0])

        self.canvas.create_line(start_x, start_y, ctrl_x, ctrl_y, end_x, end_y, 
                                arrow=tk.LAST, fill=color, width=1.5, smooth=True)


    # --- Fungsi Kontrol ---
    def get_input(self, title, prompt):
        return simpledialog.askstring(title, prompt, parent=self)

    def add_head(self):
        data_str = self.get_input("Tambah di Awal", "Masukkan nilai data:")
        if data_str:
            try:
                data = int(data_str)
                self.update_status(f"Menambahkan {data} di awal...")
                new_node = self.cdll.insert_at_head(data)
                self.animate_add(new_node)
            except ValueError:
                messagebox.showerror("Error", "Masukkan harus berupa angka.")

    def add_tail(self):
        data_str = self.get_input("Tambah di Akhir", "Masukkan nilai data:")
        if data_str:
            try:
                data = int(data_str)
                self.update_status(f"Menambahkan {data} di akhir...")
                new_node = self.cdll.insert_at_tail(data)
                self.animate_add(new_node)
            except ValueError:
                messagebox.showerror("Error", "Masukkan harus berupa angka.")

    def delete(self):
        data_str = self.get_input("Hapus Node", "Masukkan nilai yang akan dihapus:")
        if data_str:
            try:
                data = int(data_str)
                node_to_delete, prev_node = self.cdll.delete_node(data)
                if node_to_delete:
                    self.update_status(f"Menghapus node {data}...")
                    self.animate_delete(node_to_delete, prev_node)
                else:
                    self.update_status(f"Node {data} tidak ditemukan!", "red")
            except ValueError:
                messagebox.showerror("Error", "Masukkan harus berupa angka.")

    def find(self):
        data_str = self.get_input("Cari Node", "Masukkan nilai yang akan dicari:")
        if data_str:
            try:
                data = int(data_str)
                self.update_status(f"Mencari node {data}...")
                self.animate_find(data)
            except ValueError:
                messagebox.showerror("Error", "Masukkan harus berupa angka.")
                
    # --- Fungsi Animasi ---
    def animate_add(self, new_node):
        # Redraw list with new node positions but highlight the new one
        self.calculate_positions()
        
        # Animate the new node appearing
        new_pos = self.node_positions[new_node]
        self.draw_list() # draw old state first
        self.update()
        time.sleep(0.5)

        self.draw_list(highlight_node=new_node, color="lightgreen")
        self.update()
        time.sleep(1)
        
        self.draw_list() # Final state
        self.update_status(f"Node {new_node.data} berhasil ditambahkan.")
        
    def animate_delete(self, deleted_node, prev_node):
        # Draw list with node to be deleted highlighted in red
        self.draw_list(highlight_node=deleted_node, color="salmon")
        self.update()
        time.sleep(1)
        
        # Redraw without the deleted node
        self.draw_list()
        self.update()
        self.update_status(f"Node {deleted_node.data} berhasil dihapus.")

    def animate_find(self, key):
        nodes = self.cdll.get_nodes()
        if not nodes:
            self.update_status(f"List kosong, node {key} tidak ditemukan.", "red")
            return
            
        found = False
        for node in nodes:
            self.draw_list(highlight_node=node, color="yellow")
            self.update()
            time.sleep(0.7)
            
            if node.data == key:
                self.update_status(f"Node {key} ditemukan!", "green")
                self.draw_list(highlight_node=node, color="lightgreen")
                found = True
                break
        
        if not found:
            self.update_status(f"Node {key} tidak ditemukan.", "red")
            self.draw_list()

# --- Main Program ---
if __name__ == "__main__":
    app = App()
    app.mainloop()