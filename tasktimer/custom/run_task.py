import streamlit.components.v1 as components


def import_run_task(user_timezone, hours_minutes, desc, priority, limit_timer,
                    audio_source_done, audio_source_click):
    # HTML + JavaScript таймер с ограничением
    timer_html = f"""
          <style>
              .button_close {{
                color: inherit;
                border-radius: 0.5rem;
                font-size: 1rem;
                cursor: pointer;
                transition: background-color 0.2s ease-in-out, transform 0.1s ease-in-out;
                border: 2px solid rgb(231 154 149);
                padding: 0.25rem 0.75rem;
                min-height: 2.5rem;
              }}

              .button_close:hover {{
                color: red;
                border: 2px solid rgb(229 76 66);;
              }}

              .button_close:active {{
                transform: scale(0.95);
              }}

              /* ---------- appear Done state ---------- */
              #result {{
                position: relative;
                left: -150px;    /* Начальная позиция элемента */
                opacity: 0;      /* Элемент скрыт */
                transition: left 0.5s ease-out, opacity 0.5s ease-out;  /* Переход для анимации */
              }}
              /* -------------------- */
          </style>

        <script>
            // format = 'Europe/Kiev'
            const user_timezone = "{user_timezone}";
        
            const task_start_datetime = getLocalDateTime();
            const hours_minutes = "{hours_minutes}";
            const desc = "{desc}";
            const priority = {priority};
                       
            var limit = {limit_timer} * 1000;  // Общее время в миллисекундах
            var startTime = null;  // Время начала отсчета
            var remainingTime = limit;  // Сколько времени осталось
            var timerRunning = false;
            var timerPaused = false;
            var timerInterval = null;

            function formatTime(ms) {{
                var totalSeconds = Math.floor(ms / 1000);
                var minutes = String(Math.floor(totalSeconds / 60)).padStart(2, '0');
                var seconds = String(totalSeconds % 60).padStart(2, '0');
                return minutes + ":" + seconds;
            }}
          
            function getLocalDateTime() {{
                    const now = new Date();
                
                    // Опции форматирования с указанием часового пояса
                    const options = {{
                        timeZone: user_timezone,
                        year: 'numeric',
                        month: '2-digit',
                        day: '2-digit',
                        hour: '2-digit',
                        minute: '2-digit',
                        second: '2-digit',
                        hour12: false, // 24-часовой формат
                    }};
                
                    // Получаем разбитые части даты
                    const formatter = new Intl.DateTimeFormat('en-GB', options);
                    const parts = formatter.formatToParts(now);
                
                    // Извлекаем нужные части
                    let day, month, year, hour, minute, second;
                    for (const part of parts) {{
                        if (part.type === "day") day = part.value;
                        if (part.type === "month") month = part.value;
                        if (part.type === "year") year = part.value;
                        if (part.type === "hour") hour = part.value;
                        if (part.type === "minute") minute = part.value;
                        if (part.type === "second") second = part.value;
                    }}
                
                    // Собираем итоговую строку
                    return `${{year}}-${{month}}-${{day}} ${{hour}}:${{minute}}:${{second}}`;
                }}
                
            // -----------------------------------
            
            function updateTimer() {{
                if (!timerRunning || timerPaused) return;

                var elapsedTime = Date.now() - startTime;
                var timeLeft = remainingTime - elapsedTime;

                if (timeLeft <= 0) {{
                    const task_end_datetime = getLocalDateTime();
                
                    // play mp3 Done
                    document.getElementById("audio_done").play();
                    
                    document.getElementById("timer").innerText = formatTime(0);
                    clearInterval(timerInterval);
                    timerRunning = false;

                    // Устанавливаем куки о завершении задачи
                    // "hours_minutes", "desc", "priority", task_start_datetime, task_end_datetime
                     
                    document.cookie = `task_is_created=1; path=/`;
                    document.cookie = `task_start_datetime=${{task_start_datetime}}; path=/`;
                    document.cookie = `task_end_datetime=${{task_end_datetime}}; path=/`;
                    document.cookie = `hours_minutes=${{hours_minutes}}; path=/`;
                    document.cookie = `desc=${{desc}}; path=/`;
                    document.cookie = `priority=${{priority}}; path=/`;
                    
                    document.getElementById("toggleBtn").style.display = "none";

                    // appear "Task Completed".
                    var element = document.getElementById("result");
                    element.innerText = "Task Completed";
                    element.style.left = '0px';    // Двигаем на 100px вправо
                    element.style.opacity = '1';   // Делаем элемент видимым
                    
                    // update text button to 'Close'
                    var button_cancel = Array.from(window.parent.document.querySelectorAll("button")).find(
                                                   b => b.innerText.includes("Cancel"));
                    button_cancel.innerText = "Close"
                    
                    return;
                }}

                document.getElementById("timer").innerText = formatTime(timeLeft);
            }}

            function toggleTimer() {{

                if (!timerRunning) {{
                    // Запуск таймера
                    startTime = Date.now();
                    timerRunning = true;
                    timerPaused = false;
                    document.getElementById("toggleBtn").innerHTML = "⏸️"; // Меняем иконку на паузу
                    timerInterval = setInterval(updateTimer, 100);
                }} else if (!timerPaused) {{
                    // Пауза
                    // play mp3 Click
                    document.getElementById("audio_click").play();

                    remainingTime -= (Date.now() - startTime);
                    timerPaused = true;
                    clearInterval(timerInterval);
                    document.getElementById("toggleBtn").innerHTML = "▶️"; // Меняем иконку на старт
                }} else {{
                    // Продолжение

                    // play mp3 Click
                    document.getElementById("audio_click").play();

                    startTime = Date.now();
                    timerPaused = false;
                    document.getElementById("toggleBtn").innerHTML = "⏸️"; // Меняем иконку на паузу
                    timerInterval = setInterval(updateTimer, 100);
                }}
            }}

            // Автозапуск таймера
            setTimeout(toggleTimer, 500);


        // --------------------
        </script>

        <p id="timer" style="font-size: 70px;
                            text-align: center;
                            margin: 0px;
                            color: #c1bcbc;
                            font-weight: bold;
                            text-shadow: 2px 0 #6c6b6b, -2px 0 #706d6d, 0 2px #6c6767,
                                         0 -2px #5c5858, 1px 1px #605c5c, -1px -1px #504e4e,
                                         1px -1px #6e6a6a, -1px 1px #5e5c5c;">00:00</p>

        <div style="text-align: center;">
            <button id="toggleBtn" onclick="toggleTimer()" style="font-size: 20px;
                                                                     padding: 10px;
                                                                      margin: 5px;
                                                                      border-radius: 25px;
                                                                      border: 1px solid rgb(137, 133, 133);
                                                                      ">⏸</button>
        </div>

         <div>
            <h2 id="result" style="color: rgb(41 124 41); text-align: center; font-size: 30px;"></h2>
         </div>

         <audio id="audio_done">
            <source src="{audio_source_done}" type="audio/mp3">
         </audio>

         <audio id="audio_click">
            <source src="{audio_source_click}" type="audio/mp3">
         </audio>

    """
    components.html(timer_html, height=215)

