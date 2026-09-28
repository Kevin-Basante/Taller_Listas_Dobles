import tkinter as tk
from tkinter import messagebox

class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def insert_at_position(self, data, position):
        new_node = Node(data)
        
        if position <= 0:
            if not self.head:
                self.head = new_node
                self.tail = new_node
            else:
                new_node.next = self.head
                self.head.prev = new_node
                self.head = new_node
            return True

        current = self.head
        current_pos = 0

        while current and current_pos < position:
            current = current.next
            current_pos += 1

        if not current:
            if not self.head:
                self.head = new_node
                self.tail = new_node
            else:
                self.tail.next = new_node
                new_node.prev = self.tail
                self.tail = new_node
        else:
            new_node.prev = current.prev
            new_node.next = current
            if current.prev:
                current.prev.next = new_node
            else:
                self.head = new_node
            current.prev = new_node
        return True

    def remove_at_position(self, position):
        if not self.head:
            return None

        current = self.head
        current_pos = 0

        while current and current_pos < position:
            current = current.next
            current_pos += 1

        if not current:
            return None

        data = current.data

        if current.prev:
            current.prev.next = current.next
        else:
            self.head = current.next

        if current.next:
            current.next.prev = current.prev
        else:
            self.tail = current.prev

        return data

    def get_gallery_route(self):
        items = []
        current = self.head
        while current:
            items.append(current.data)
            current = current.next
        return items

class GalleryExhibitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Art Gallery Exhibition Router")
        self.root.geometry("500x700")
        self.root.config(bg="#1c1c1e")
        
        self.gallery = DoublyLinkedList()

        header_frame = tk.Frame(root, bg="#1c1c1e")
        header_frame.pack(pady=25)
        
        tk.Label(header_frame, text="Exhibition Route Manager", bg="#1c1c1e", fg="#d4af37", font=("Helvetica", 18, "bold")).pack()
        tk.Label(header_frame, text="Double Linked List Tracker", bg="#1c1c1e", fg="#8e8e93", font=("Helvetica", 10)).pack()

        input_frame = tk.Frame(root, bg="#1c1c1e")
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Artwork:", bg="#1c1c1e", fg="#ffffff", font=("Helvetica", 11)).grid(row=0, column=0, padx=5, pady=5)
        self.entry_artwork = tk.Entry(input_frame, width=20, font=("Helvetica", 11), bg="#2c2c2e", fg="#ffffff", insertbackground="white", relief="flat")
        self.entry_artwork.grid(row=0, column=1, padx=5, pady=5, ipady=3)

        tk.Label(input_frame, text="Position:", bg="#1c1c1e", fg="#ffffff", font=("Helvetica", 11)).grid(row=1, column=0, padx=5, pady=5)
        self.entry_position = tk.Entry(input_frame, width=20, font=("Helvetica", 11), bg="#2c2c2e", fg="#ffffff", insertbackground="white", relief="flat")
        self.entry_position.grid(row=1, column=1, padx=5, pady=5, ipady=3)

        button_frame = tk.Frame(root, bg="#1c1c1e")
        button_frame.pack(pady=15)

        tk.Button(button_frame, text="Insert at Position", bg="#34c759", fg="white", font=("Helvetica", 10, "bold"), width=16, relief="flat", command=self.insert_route).grid(row=0, column=0, padx=10, pady=5)
        tk.Button(button_frame, text="Remove from List", bg="#ff3b30", fg="white", font=("Helvetica", 10, "bold"), width=16, relief="flat", command=self.remove_route).grid(row=0, column=1, padx=10, pady=5)

        tk.Label(root, text="Bilateral Exhibition Flow:", bg="#1c1c1e", fg="#d4af37", font=("Helvetica", 12, "bold")).pack(pady=5)
        
        self.listbox = tk.Listbox(root, font=("Courier", 12, "bold"), width=40, height=14, bg="#2c2c2e", fg="#ffffff", selectbackground="#d4af37", relief="flat", highlightthickness=0, justify="center")
        self.listbox.pack(pady=10)
        self.refresh_display()

    def insert_route(self):
        artwork = self.entry_artwork.get().strip()
        pos_str = self.entry_position.get().strip()
        
        if not artwork:
            messagebox.showwarning("Input Required", "Please enter an artwork name.")
            return
            
        try:
            position = int(pos_str) if pos_str else 0
        except ValueError:
            messagebox.showerror("Invalid Input", "Position must be an integer.")
            return

        self.gallery.insert_at_position(artwork, position)
        self.entry_artwork.delete(0, tk.END)
        self.entry_position.delete(0, tk.END)
        self.refresh_display()

    def remove_route(self):
        selection = self.listbox.curselection()
        
        if selection:
            listbox_index = selection[0]
            route = self.gallery.get_gallery_route()
            
            if not route:
                return
                
            num_artworks = len(route)
            
            if listbox_index < 2 or listbox_index >= 2 + (num_artworks * 2) - 1:
                 messagebox.showwarning("Invalid Selection", "Please select a valid artwork node.")
                 return
                 
            if listbox_index % 2 != 0:
                 messagebox.showwarning("Invalid Selection", "You selected a pointer. Please select an artwork node.")
                 return
            
            node_position = (listbox_index - 2) // 2
            
            removed = self.gallery.remove_at_position(node_position)
            if removed is None:
                messagebox.showerror("Error", "Could not remove selected item.")
            
        else:
            pos_str = self.entry_position.get().strip()
            if not pos_str:
                messagebox.showwarning("Input Required", "Select an item in the list or enter a position.")
                return
                
            try:
                position = int(pos_str)
            except ValueError:
                messagebox.showerror("Invalid Input", "Position must be an integer.")
                return
                
            removed = self.gallery.remove_at_position(position)
            if removed is None:
                messagebox.showinfo("Not Found", "No artwork found at that position.")
                
        self.refresh_display()

    def refresh_display(self):
        self.listbox.delete(0, tk.END)
        route = self.gallery.get_gallery_route()
        
        if not route:
            self.listbox.insert(tk.END, "")
            self.listbox.insert(tk.END, "[ Empty Route ]")
            return

        self.listbox.insert(tk.END, "(NULL)")
        self.listbox.insert(tk.END, "⇅")
        
        for i, artwork in enumerate(route):
            self.listbox.insert(tk.END, f"[ {artwork} ]")
            if i < len(route) - 1:
                self.listbox.insert(tk.END, "⇅")
                
        self.listbox.insert(tk.END, "⇅")
        self.listbox.insert(tk.END, "(NULL)")

if __name__ == "__main__":
    window = tk.Tk()
    app = GalleryExhibitionApp(window)
    window.mainloop()