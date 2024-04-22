import tkinter as tk
import webbrowser


def open_url(event=None):
    webbrowser.open_new_tab("https://www.education.gov.in/nep/about-nep")

def change_cursor_enter(event):
    event.widget.config(cursor="hand2")  # Change cursor to hand pointer when entering
def change_cursor_leave(event):
    event.widget.config(cursor="")
    
def load_and_place_images(canvas, image_paths, positions):
    images = []  # To keep references to images to prevent garbage collection
    for path, position in zip(image_paths, positions):
        try:
            img = tk.PhotoImage(file=path)
            canvas.create_image(position, image=img, anchor="center")
            images.append(img)  # Keep a reference to prevent GC
        except tk.TclError as e:
            print(f"Error loading image {path}: {e}")
    return images

def draw_nep_text(canvas):
    canvas.create_text(350, 370, text="NATIONAL", font=("Helvetica", 33, "bold"), fill="black")
    canvas.create_text(350, 420, text=" EDUCATION ", font=("Helvetica", 33, "bold"), fill="black")
    canvas.create_text(350, 470, text="POLICY ", font=("Helvetica", 33, "bold"), fill="black")
    canvas.create_text(350, 520, text="2020", font=("Helvetica", 33, "bold"), fill="black")
    canvas.create_line(210, 395, 490, 395, fill="white", width=2)
    canvas.create_line(210, 445, 490, 445, fill="white", width=2)
    canvas.create_text(200, 20, text="Why is it important?", font=("Helvetica", 20), fill="black")
    canvas.create_text(850, 300, text="What has changed?", font=("Helvetica", 20), fill="black")

def draw_timeline(canvas, coordinates, years, descriptions):
    # Draw the connecting lines first
    for i in range(len(coordinates) - 1):
        canvas.create_line(coordinates[i][0], coordinates[i][1], coordinates[i+1][0], coordinates[i+1][1], fill='white', width=5)

    # Draw the circles and text
    for (x, y), year, description in zip(coordinates, years, descriptions):
        # Circle
        canvas.create_oval(x - 30, y - 30, x + 30, y + 30, fill='orange', outline='white')
        # Year text
        canvas.create_text(x, y, text=str(year), fill='black')
        # Description text
        canvas.create_text(x, y + 50, text=description)
        

    
def slide_box(canvas, x1, y1, x2, y2, fill_color, text, delay, interval=20, steps=50):
    
    start_x1 = -x2  # Start off-screen to the left
    # Create the box and text off-screen
    box_id = canvas.create_rectangle(start_x1, y1, start_x1 + (x2 - x1), y2, outline='black', fill=fill_color, width=2)
    text_id = canvas.create_text(start_x1 + (x2 - x1) / 2, (y1 + y2) / 2, text=text, fill="white", font=("Helvetica", 12))

    def animate(step):
        if step <= steps:
            # Calculate the distance to move for each step
            dx = (x1 - start_x1) / steps
            canvas.move(box_id, dx, 0)
            canvas.move(text_id, dx, 0)
            canvas.after(interval, lambda: animate(step + 1))
    
    # Start the animation with the specified delay
    canvas.after(delay, lambda: animate(0))

def animate_boxes(canvas, box_coords, colors, texts, start_interval=1000):
    """
    Animate the appearance of colored boxes sliding in one by one, with each box starting after 'start_interval'.
    """
    for i, ((x1, y1, x2, y2), color, text) in enumerate(zip(box_coords, colors, texts)):
        # Calculate the delay for each box based on its order
        delay = i * start_interval
        slide_box(canvas, x1, y1, x2, y2, color, text, delay)

class ToolTip:
    def __init__(self, widget):
        self.widget = widget
        self.tip_window = None

    def show_tip(self, tip_text, x, y):
        if self.tip_window or not tip_text:
            return
        
        self.tip_window = tk.Toplevel(self.widget)
        self.tip_window.wm_overrideredirect(True)
        self.tip_window.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(self.tip_window, text=tip_text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)
        
    def hide_tip(self):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None  

def animate_rectangles(canvas, start_x, start_y, num_rectangles, interval, start_delay, step_x, step_y, fill_colors, texts, tooltips, toolTip):
    def draw_rectangle(index):
        if index < num_rectangles:
            x, y = start_x + index * step_x, start_y + index * step_y
            fill_color = fill_colors[index] if index < len(fill_colors) else 'white'
            text_content = texts[index] if index < len(texts) else "No text"
            tooltip_text = tooltips[index] if index < len(tooltips) else ""
            tag = f"rect_{index}"  # Unique tag for each rectangle and its text
            
            # Create the rectangle and text with the same tag
            rect_id = canvas.create_rectangle(x, y, x + 600, y + 70, outline="black", fill=fill_color, width=2, tags=tag)
            text_id = canvas.create_text(x + 300, y + 35, text=text_content, fill="white", font=("Helvetica", 12), tags=tag)
            
            def on_enter(event, text=tooltip_text):
                x1, y1, x2, y2 = canvas.bbox(tag)  # Get the bounding box of the tagged items
                tooltip_x = x1 - 160  # Position the tooltip 10 pixels to the left of the rectangle's left edge
                tooltip_y = y1
                toolTip.show_tip(text, tooltip_x, tooltip_y)

            def on_leave(event):
                toolTip.hide_tip()
            

            # Bind the enter and leave events to the tag, affecting both rectangle and text
            canvas.tag_bind(tag, '<Enter>', on_enter)
            canvas.tag_bind(tag, '<Leave>', on_leave)

            if index + 1 < num_rectangles:
                canvas.after(interval, lambda: draw_rectangle(index + 1))

    canvas.after(start_delay, lambda: draw_rectangle(0))


    

def draw_window():
    
    root = tk.Tk()
    root.title("NEP POSTER")
    root.geometry("1550x800")

    canvas = tk.Canvas(root, width=1550, height=800)
    canvas.pack(fill="both", expand=True)
    
    # Load the background image
    bg_image = tk.PhotoImage(file=r"C:\Users\Mohit\Downloads\tricolor.png")
    canvas.create_image(0, 0, anchor="nw", image=bg_image)
    
    draw_nep_text(canvas)
    
    coordinates = [(100, 280), (250, 280), (400, 280), (550, 280)]
    years = [1968, 1986, 1992, 2020]
    descriptions = ["First National\nEducation Policy", "Second National\nEducation Policy", "Modified Second National\nEducation Policy", "Latest National\nEducation Policy"]
    draw_timeline(canvas, coordinates, years, descriptions)

    box_coords = [(30, 40, 320, 240), (320, 40, 610, 240), (610, 40, 900, 240), (900, 40, 1190, 240), (1190, 40, 1470, 240)]
    colors = [
    '#E31A1C',  
    '#FD7F23',  
    '#FFC400',  
    '#33A02C',  
    '#6A3D9A',  
    ]
    texts = [
    "     Holistic and Inclusive Education:\n\nEmphasizes inclusive access to\n education for all, integrating\n early childhood education and care.\n\nAdvocates for a broad-based,\n multi-disciplinary approach with a \nflexible curriculum that fosters\n overall development—cognitive,\n emotional, and ethical..",
    "Revolutionizing Teaching and Learning:\n\nFocuses on teacher recruitment and \ncontinuous professional development,\n ensuring high-quality education.\n\nShifts assessment methods to evaluate\n actual learning outcomes, \npromoting critical thinking and \ncreativity over rote memorization.",
    " Vocational and Skill Enhancement:\n\n Integrates vocational education\n with mainstream academics, focusing on\n skill development from a young age.\n\n Encourages experiential learning \n through internships and practical\n experiences, aligning with industry needs.",
    "  Technology Integration and Research\n Innovation:\n\n  Uses technology for expanding the reach \n  of education, fostering digital literacy,\n  and creating virtual learning environments.\n\n  Establishes a robust research framework\n  with the National Research Foundation\n  to nurture a culture of innovation\n  across academic institutions.",
    " Globalization and Equitable Resources:\n\n Aims for the internationalization \n of education, allowing top world\n institutions to set up campuses in India.\n\n Proposes Special Education Zones\n and efficient resource governance to\n ensure equitable education\n opportunities in underprivileged regions."
    ]
    animate_boxes(canvas, box_coords, colors, texts)
    
    rectangle_colors = [
    '#E31A1C',  
    '#FD7F23', 
    '#FFC400',  
    '#33A02C',  
    '#6A3D9A',  
    ]
    rectangle_texts = [
        "Holistic 5+3+3+4 Structure & ECCE:\n Revamps education with a child-centric structure,focusing on holistic development\n from early childhood.  Emphasizes foundational learning.",
        "Language & Vocational Education:\n Advocates for mother tongue until Grade 5 to enhance comprehension. \nIntegrates vocational training from Grade 6, preparing students with real-world skills.",
        "Flexible UG/PG Pathways & Research:\nIntroduces flexible UG programs with multiple exit points, encouraging interdisciplinary\nstudy. Focuses on research with NRF support.",
        "Tech Empowerment & Inclusive Education:\nLeverages NETF for accessible learning platforms.\nEnsures equitable education opportunities for all, focusing on disadvantaged groups.",
        "Teacher Training & Higher Ed Quality:\n Mandates 4-year integrated B.Ed., enhancing teaching quality. Establishes HECI to\n oversee standards and promote academic excellence."
    ]
    

    tooltips = [
        'The Holistic 5+3+3+4 Structure & Early Childhood Care and Education (ECCE), as outlined in India\'s National Education Policy (NEP) 2020, revamps the traditional 10+2 schooling system into a \n5+3+3+4 framework. This structure is tailored to align with the developmental stages of learners:\nFoundational Stage (5 years): Integrates three years of pre-primary education with grades 1 and 2, focusing on interactive and play-based learning methods.\nPreparatory Stage (3 years): Spans grades 3 to 5, introducing formal education through play and activity-based pedagogy.\nMiddle Stage (3 years): Covers grades 6 to 8, shifting towards a more structured subject-focused curriculum including science, arts, and humanities.\nSecondary Stage (4 years): For grades 9 to 12, offers multidisciplinary education with flexible subject choices.\nThe NEP places a strong emphasis on ECCE(Early Childhood Care and Education) to ensure foundational development for every child, aiming for holistic growth and preparing them for\n future educational endeavors and life challenges.',
        'Mother Tongue Instruction: NEP 2020 advocates for instruction in the mother tongue or local language at least until Grade 5, but preferably till Grade 8 and beyond.This approach is based \non evidence that young children learn and grasp non-trivial concepts more quickly in their home language. The policy suggests that this method enhances cognitive development and helps in \nretaining cultural identity. It also aims to mitigate the disadvantages faced by students who are not proficient in the previously mandated medium of instruction, typically English or \nHindi, thereby aiming for more equitable access to education.\nVocational Integration: Recognizing the importance of skill development, NEP 2020 plans to integrate vocational education \ninto the school curriculum from Grade 6 onwards. This early exposure to vocational training includes a range of internships and apprenticeships with local artisans, businesses, and other \nvocational experts. The goal is to provide students with hands-on learning experiences, thereby making education more relevant to employment and entrepreneurial opportunities. Vocational \ntraining is seen as a means to diversify education, reduce the stigma associated with vocational education, and equip the youth with practical skills that are increasingly necessary in the \nmodern economy.',
        'The National Education Policy (NEP) 2020 in India has introduced transformative changes in higher education, aiming to make it more flexible, interdisciplinary, and \nresearch-oriented.The policy advocates for flexible undergraduate (UG) programs that offer multiple exit options. Students can now obtain a certificate after \ncompleting one year in a discipline or field,including vocational and professional areas, or a diploma after two years of study, or a Bachelor’s degree after three years. \nThe introduction of a 4-year multidisciplinary Bachelor\'s program provides an opportunity for deeper specialization in a chosen field.\nMoreover, the NEP emphasizes the importance of interdisciplinary education, allowing students to choose their subjects freely across disciplines. This approach\n is designed to foster a broader understanding and appreciation of diverse fields, equipping students with varied skills and perspectives.\nResearch is another cornerstone of the NEP, with the establishment of the National Research Foundation (NRF) to fund and promote research across all academic disciplines. \nThe NRF aims to cultivate a strong research culture in universities and colleges, encouraging cutting-edge work in science, technology, social sciences, and humanities. \nThis is expected to drive innovation, contribute to national development, and position India as a global research hub.',
        'The National Education Policy (NEP) 2020 introduces a significant emphasis on technology integration and inclusivity in education through the creation \nof the National Educational Technology Forum (NETF). This initiative aims to leverage technology to create more accessible and inclusive learning platforms\n for students across India, focusing particularly on bridging the digital divide that exists in the educational landscape.NETF\'s mandate includes the \ndevelopment of digital infrastructure, educational software, and content that are accessible to all learners, including those from disadvantaged and marginalized \ncommunities. By fostering an ecosystem where technology enhances educational experiences, the NEP seeks to ensure that every student, regardless of their socio-economic \nstatus, has equal access to high-quality educational resources.The policy highlights the importance of adaptive technologies that support students with \ndisabilities, ensuring that education is inclusive and accommodates diverse learning needs. Moreover, it envisions leveraging technology to provide remote and rural areas \nwith the same quality of education available in urban centers, thereby addressing geographical disparities.Through initiatives like online courses,\n digital libraries, and virtual labs, NETF aims to democratize access to knowledge and learning opportunities. ',
        'A key reform is the mandate for a 4-year integrated Bachelor of Education (B.Ed.) program, designed to provide a robust foundation in pedagogy,\n subject knowledge, and practical teaching skills. This program is aimed at aspiring teachers and emphasizes the importance of preparing\n educators who are well-equipped to meet the diverse needs of students in the 21st century.Additionally, the NEP establishes the Higher Education\n Commission of India (HECI) to oversee the higher education sector, with a focus on promoting academic excellence and maintaining high\n standards. The HECI is tasked with regulating, accrediting, and ensuring governance in higher education institutions, aiming to foster an environment of innovation,\n research, and quality teaching. Its role includes streamlining academic processes, promoting autonomy, and ensuring that educational\n institutions adhere to the highest quality standards.The NEP\'s focus on teacher training and higher education quality is intended to transform the educational landscape\n by producing well-qualified, innovative, and dedicated educators. '
    ]
    

    total_delay_for_boxes = len(box_coords) * 1000 + (50 * 20)  

    toolTip = ToolTip(canvas)
   
    animate_rectangles(
    canvas, start_x=680, start_y=350, num_rectangles=5, interval=500, 
    start_delay=total_delay_for_boxes, step_x=50, step_y=80, fill_colors=rectangle_colors, 
    texts=rectangle_texts, tooltips=tooltips, toolTip=toolTip)

    # Load and place other images
    images = load_and_place_images(canvas, [
        r"C:\Users\Mohit\Downloads\nepbook-removebg-preview.png",
        r"C:\Users\Mohit\Downloads\brain-removebg-preview.png",
        r"C:\Users\Mohit\Downloads\globe-removebg-preview.png",
        r"C:\Users\Mohit\Downloads\Screenshot_2024-02-15_212052-removebg-preview.png",
        r"C:\Users\Mohit\Downloads\book.png",
        r"C:\Users\Mohit\Downloads\girl-removebg-preview.png",
        r"C:\Users\Mohit\Downloads\image-removebg-preview.png",
        r"C:\Users\Mohit\Downloads\image-removebg-preview (1).png"
    ], [(350, 560), (600, 670),(100, 670),(550, 490),(150,490), (710, 300), (35, 102),(1395,510)])

    text = canvas.create_text(350, 750, text="Learn More About NEP 2020", font=("Helvetica", 12, "underline"), fill="blue", tags="url")
    canvas.tag_bind(text, "<Enter>", change_cursor_enter)
    canvas.tag_bind(text, "<Leave>", change_cursor_leave)
    canvas.tag_bind(text, "<Button-1>", open_url)
    
    # Keep a reference to the background image to prevent garbage collection
    canvas.bg_image = bg_image
    canvas.images = images  # Keep references to additional images

    # Run the Tkinter event loop
    root.mainloop()

# Call the function to draw the window
draw_window()


