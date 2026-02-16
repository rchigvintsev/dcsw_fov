import tkinter as tk
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class FOVCalculatorApp:
    """Приложение для расчёта и визуализации настроек оси FOV в игре DCS World"""
    
    # Значения по умолчанию
    DEFAULT_MIN_FOV = 20
    DEFAULT_MAX_FOV = 140
    
    # Цветовые схемы
    LIGHT_THEME = {
        'bg': '#f0f0f0',
        'fg': '#000000',
        'entry_bg': '#ffffff',
        'entry_fg': '#000000',
        'text_bg': '#ffffff',
        'text_fg': '#000000',
        'plot_bg': '#ffffff',
        'plot_fg': '#000000',
        'grid_color': '#cccccc',
        'line_color': '#1f77b4',
        'annotation_bg': '#ffff99'
    }
    
    DARK_THEME = {
        'bg': '#2b2b2b',
        'fg': '#ffffff',
        'entry_bg': '#3c3f41',
        'entry_fg': '#ffffff',
        'text_bg': '#313335',
        'text_fg': '#ffffff',
        'plot_bg': '#2b2b2b',
        'plot_fg': '#ffffff',
        'grid_color': '#555555',
        'line_color': '#4a9eff',
        'annotation_bg': '#5a5a00'
    }
    
    def __init__(self, root):
        self.root = root
        self.root.title("DCS World FOV Calculator")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Текущая тема (по умолчанию светлая)
        self.is_dark_theme = False
        self.current_theme = self.LIGHT_THEME
        
        # Настройка стиля
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self._create_widgets()
        self._apply_theme()
        self._calculate_and_plot()
    
    def _create_widgets(self):
        """Создание элементов интерфейса"""
        
        # Основной контейнер
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Настройка растягивания
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Панель ввода параметров
        input_frame = ttk.LabelFrame(main_frame, text="Параметры FOV", padding="10")
        input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # MIN_FOV
        ttk.Label(input_frame, text="Min FOV:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.min_fov_var = tk.StringVar(value=str(self.DEFAULT_MIN_FOV))
        self.min_fov_entry = ttk.Entry(input_frame, textvariable=self.min_fov_var, width=15)
        self.min_fov_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # MID_FOV
        ttk.Label(input_frame, text="Mid FOV:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.mid_fov_var = tk.StringVar(value="80")
        self.mid_fov_entry = ttk.Entry(input_frame, textvariable=self.mid_fov_var, width=15)
        self.mid_fov_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # MAX_FOV
        ttk.Label(input_frame, text="Max FOV:").grid(row=0, column=4, sticky=tk.W, padx=5, pady=5)
        self.max_fov_var = tk.StringVar(value=str(self.DEFAULT_MAX_FOV))
        self.max_fov_entry = ttk.Entry(input_frame, textvariable=self.max_fov_var, width=15)
        self.max_fov_entry.grid(row=0, column=5, padx=5, pady=5)
        
        # Кнопка расчета
        self.calc_button = ttk.Button(input_frame, text="Рассчитать", command=self._calculate_and_plot)
        self.calc_button.grid(row=0, column=6, padx=15, pady=5)
        
        # Переключатель темы
        self.theme_button = ttk.Button(input_frame, text="🌙 Тёмная тема", command=self._toggle_theme)
        self.theme_button.grid(row=0, column=7, padx=5, pady=5)
        
        # Панель графика
        graph_frame = ttk.LabelFrame(main_frame, text="График настройки оси FOV", padding="10")
        graph_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        graph_frame.columnconfigure(0, weight=1)
        graph_frame.rowconfigure(0, weight=1)
        
        # Создание графика
        self.figure = Figure(figsize=(8, 5), dpi=100)
        self.ax = self.figure.add_subplot(111)
        
        self.canvas = FigureCanvasTkAgg(self.figure, master=graph_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Панель результатов
        result_frame = ttk.LabelFrame(main_frame, text="Значения для настройки", padding="10")
        result_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.result_text = tk.Text(result_frame, height=3, width=80, wrap=tk.WORD)
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Скроллбар для текста
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.result_text.configure(yscrollcommand=scrollbar.set)
    
    def _calculate_fov_values(self, min_fov, mid_fov, max_fov):
        """Расчёт значений FOV"""
        result = []
        
        mid = (mid_fov - min_fov) / ((max_fov - min_fov) / 100.0)
        result.append(round(mid))
        left = right = mid
        decr = mid / 5
        incr = (100 - mid) / 5
        
        for i in range(5):
            left = max(left - decr, 0)
            result.insert(0, round(left))
            
            right = min(right + incr, 100)
            result.append(round(right))
        
        return result
    
    def _calculate_and_plot(self):
        """Расчёт и отображение графика"""
        try:
            # Получение значений
            min_fov = float(self.min_fov_var.get())
            mid_fov = float(self.mid_fov_var.get())
            max_fov = float(self.max_fov_var.get())
            
            # Валидация
            if min_fov >= mid_fov or mid_fov >= max_fov:
                self._show_error("Ошибка: min_fov < mid_fov < max_fov")
                return
            
            if min_fov < 0 or max_fov > 180:
                self._show_error("Ошибка: FOV должен быть в диапазоне 0-180")
                return
            
            # Расчет значений
            result = self._calculate_fov_values(min_fov, mid_fov, max_fov)
            
            # Обновление графика
            self._update_plot(result, min_fov, mid_fov, max_fov)
            
            # Обновление текстового результата
            self._update_result_text(result)
            
        except ValueError:
            self._show_error("Ошибка: введите корректные числовые значения")
    
    def _update_plot(self, result, min_fov, mid_fov, max_fov):
        """Обновление графика"""
        theme = self.current_theme
        
        self.ax.clear()
        
        # Настройка цветов графика
        self.figure.patch.set_facecolor(theme['plot_bg'])
        self.ax.set_facecolor(theme['plot_bg'])
        
        # Позиции точек (11 точек от 0 до 10)
        positions = list(range(11))
        
        # Построение графика
        self.ax.plot(positions, result, color=theme['line_color'], marker='o', 
                    linewidth=2, markersize=8, label='Кривая оси')
        self.ax.grid(True, alpha=0.3, color=theme['grid_color'])
        
        # Настройка осей
        self.ax.set_xlabel('Позиция на оси джойстика', fontsize=11, color=theme['plot_fg'])
        self.ax.set_ylabel('Значение (%)', fontsize=11, color=theme['plot_fg'])
        self.ax.set_title(f'График настройки FOV (min={min_fov}°, mid={mid_fov}°, max={max_fov}°)',
                         fontsize=12, fontweight='bold', color=theme['plot_fg'])
        
        # Цвет меток осей
        self.ax.tick_params(axis='x', colors=theme['plot_fg'])
        self.ax.tick_params(axis='y', colors=theme['plot_fg'])
        
        # Цвет рамки
        for spine in self.ax.spines.values():
            spine.set_edgecolor(theme['plot_fg'])
        
        # Установка диапазона
        self.ax.set_xlim(-0.5, 10.5)
        self.ax.set_ylim(-5, 105)
        
        # Установка всех меток по оси X
        self.ax.set_xticks(positions)
        
        # Добавление значений на точки
        for i, (pos, val) in enumerate(zip(positions, result)):
            self.ax.annotate(f'{val}', 
                           xy=(pos, val), 
                           xytext=(0, 10), 
                           textcoords='offset points',
                           ha='center',
                           fontsize=9,
                           color=theme['plot_fg'],
                           bbox=dict(boxstyle='round,pad=0.3', 
                                   facecolor=theme['annotation_bg'], 
                                   edgecolor=theme['plot_fg'],
                                   alpha=0.7))
        
        # Настройка легенды
        legend = self.ax.legend(loc='upper left')
        legend.get_frame().set_facecolor(theme['plot_bg'])
        legend.get_frame().set_edgecolor(theme['plot_fg'])
        for text in legend.get_texts():
            text.set_color(theme['plot_fg'])
        
        self.figure.tight_layout()
        self.canvas.draw()
    
    def _update_result_text(self, result):
        """Обновление текстового результата"""
        self.result_text.delete(1.0, tk.END)
        result_str = f"Значения для настройки оси FOV:\n{result}\n\n"
        result_str += "Используйте эти значения для настройки кривой оси в DCS World"
        self.result_text.insert(1.0, result_str)
    
    def _show_error(self, message):
        """Отображение сообщения об ошибке"""
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(1.0, message)
    
    def _toggle_theme(self):
        """Переключение между светлой и тёмной темой"""
        self.is_dark_theme = not self.is_dark_theme
        self.current_theme = self.DARK_THEME if self.is_dark_theme else self.LIGHT_THEME
        
        # Обновление текста кнопки
        if self.is_dark_theme:
            self.theme_button.configure(text="☀️ Светлая тема")
        else:
            self.theme_button.configure(text="🌙 Тёмная тема")
        
        self._apply_theme()
        self._calculate_and_plot()
    
    def _apply_theme(self):
        """Применение цветовой схемы к интерфейсу"""
        theme = self.current_theme
        
        # Настройка стилей ttk
        self.style.configure('TFrame', background=theme['bg'])
        self.style.configure('TLabelFrame', background=theme['bg'], foreground=theme['fg'])
        self.style.configure('TLabelFrame.Label', background=theme['bg'], foreground=theme['fg'])
        self.style.configure('TLabel', background=theme['bg'], foreground=theme['fg'])
        self.style.configure('TButton', background=theme['bg'], foreground=theme['fg'])
        self.style.configure('TEntry', fieldbackground=theme['entry_bg'], foreground=theme['entry_fg'])
        
        # Настройка главного окна
        self.root.configure(bg=theme['bg'])
        
        # Настройка текстового поля
        self.result_text.configure(
            bg=theme['text_bg'],
            fg=theme['text_fg'],
            insertbackground=theme['text_fg']
        )


def main():
    """Точка входа в приложение"""
    root = tk.Tk()
    FOVCalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
