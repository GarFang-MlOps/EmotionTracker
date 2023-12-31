# ML System Design Doc - [RU]
## Дизайн ML системы - \<Детектор выгорания, отслеживание динамики негативных эмоций (EmotionTracker)\> \<0.1\>
<p align="center">
  <img width="704" height="205" src="https://github.com/GarFang-MlOps/EmotionTracker/blob/main//docs/imgs/1-s2.0-S2665963823000970-gr4.jpg">
</p>

*Шаблон ML System Design Doc от телеграм-канала [Reliable ML](https://t.me/reliable_ml)*   

- Рекомендации по процессу заполнения документа (workflow) - [здесь](https://github.com/IrinaGoloshchapova/ml_system_design_doc_ru/blob/main/ML_System_Design_Doc_Workflow.md).  
- Детальный доклад о том, что такое ML System Design Doc и о том, как, когда и зачем его составлять - [тут](https://www.youtube.com/watch?v=PW9TGNr1Vqk).
    
> ## Термины и пояснения
> - Итерация - это все работы, которые совершаются до старта очередного пилота  
> - БТ - бизнес-требования 
> - EDA - Exploratory Data Analysis - исследовательский анализ данных  
> - `Product Owner`,  `Data Scientist` - роли, которые заполняют соответствующие разделы 
> - В этом шаблоне роль `Data Scientist` совмещает в себе компетенции классического `Data Scientist` с упором на исследования и `ML Engineer` & `ML Ops` роли с акцентом на продуктивизацию моделей
> - Для вашей организации распределение ролей может быть уточнено в зависимости от операционной модели 

### 1. Цели и предпосылки 
#### 1.1. Зачем идем в разработку продукта?  

**Бизнес-цель:** 
Разработка проекта **EmotionTracker** направлена на управления психическим здоровьем с помощью AI, предоставляя инструменты для персонализированного мониторинга эмоционального состояния. Проект направлен на предоставление пользователям возможности регулярно оценивать своё эмоциональное состояние, используя анализ фотографий с помощью нейронных сетей, что дает возможность раннего обнаружения психологических проблем и повышения самосознания пользователей.

**Основная идея:**
Использование AI для анализа эмоционального состояния через фотографии поможет пользователям лучше понимать свои эмоции и выявлять признаки эмоционального выгорания на ранних этапах, что сложно достигнуть традиционными методами самооценки. Пользователи получат доступ к инструменту, способному в реальном времени анализировать изменения их эмоционального фона, что способствует более эффективному управлению стрессом и эмоциональным здоровьем. 
Преимущества отслеживания настроения с помощью AI: 
- персонализированная психиатрическая помощь;
- раннее выявление проблем с психическим здоровьем;
- повышенное самосознание;
- непрерывный мониторинг.

**Успех проекта:** 
Успех определяется улучшением качества жизни пользователей, снижением уровня эмоционального выгорания и положительной обратной связью от пользователей и их активном использовании системы. Важно сочетание AI-технологий с экспертным человеческим (псхологам, психоаналитком) для достижения наилучших результатов.

#### 1.2. Бизнес-требования и ограничения

- **Бизнес-требования**:
   - **Целевое видение**: Разработка AI-системы для анализа эмоционального состояния через обработку фотографий пользователей, отправляемых через телеграм-бота. Система должна предоставлять информацию о вероятном эмоциональном состоянии пользователя и динамику изменений его состояния.
   - **Документация**: Детальные бизнес-требования будут определены и документированы в соответствии с входными данными в данном документе.

- **Бизнес-ограничения**:
   - Ограничения включают соблюдение политики конфиденциальности данных, ресурсные ограничения на разработку и внедрение, ограниченный бюджет, а также требования к этическим стандартам в области обработки персональных данных.

- **Ожидания от итерации**:
   - Реализация прототипа системы с базовыми функциями анализа эмоций и визуализацией динамики эмоционального состояния, обеспечение надежности и юзабилити продукта.

- **Бизнес-процесс пилота**:
   - Интеграция системы с телеграм-ботом для сбора и обработки фотографий пользователей, тестирование в контролируемых условиях с ограниченным числом пользователей.

- **Критерии успешности пилота**:
   - Успешный пилот характеризуется высокой точностью определения эмоционального состояния, положительными отзывами пользователей, способностью системы предоставлять полезные инсайты, и возможностью масштабирования системы.
   - Возможные пути развития включают расширение функционала путем добавления для анализа текстовой информации, например, переписок в соц. сетях, мессенджерах etc; улучшение алгоритмов анализа и интеграцию с другими платформами для широкого внедрения.
     
#### 1.3. Что входит в скоуп проекта/итерации, что не входит   

- **На закрытие каких БТ подписываемся в данной итерации `Data Scientist`**:
  - Разработка базовой модели машинного обучения для анализа эмоций на основе фотографий.
  - Проведение первичных тестов модели на выборочном наборе данных.
  - Оценка корреляции предсказаний модели с самооценками пользователей.

- **Что не будет закрыто `Data Scientist`**:
  - Интеграция модели в существующие внутренние системы.
  - Создание полноценного дэшборда для визуализации результатов модели.

- **Описание результата с точки зрения качества кода и воспроизводимости решения `Data Scientist`**:
  - Код должен быть чистым, хорошо документированным и позволять легко воспроизвести результаты.
  - Модель должна быть готова к демонстрации основных функций и проста в использовании для первых пользовательских тестов.

- **Описание планируемого технического долга (что оставляем для дальнейшей продуктивизации) `Data Scientist`**:
  - Улучшение точности и надежности модели.
  - Разработка дополнительных функций для улучшения пользовательского опыта и внедрение системы в более широкий контекст использования. 

#### 1.4. Предпосылки решения  

- **Используемые блоки данных**: Используются фотографии пользователей для анализа эмоционального состояния. Фотографии обрабатываются с использованием ResNet и haarcascade для распознавания лиц и анализа эмоций.
- **Горизонт прогноза**: Система предоставляет мгновенный анализ эмоционального состояния на основе каждой отправленной фотографии.
- **Гранулярность модели**: Анализ на уровне отдельной фотографии, предоставление индивидуальных результатов.
- **Инфраструктура и инструменты**: Использование SQLite для хранения предиктов модели (positive/negative), разработка в Jupyter Notebook с применением PyTorch, Python 3, OpenCV.
- **Документация и разработка**: Репозиторий проекта в GitHub, с документацией в Google Docs/Disk, включающей описание алгоритма и результаты тестирования.

### 2. Методология `Data Scientist`     

#### 2.1. Постановка задачи  

- **Техническая Постановка Задачи**: Разработка системы анализа эмоций на основе обработки фотографий с использованием технологий машинного обучения. Проект предполагает реализацию модели, которая классифицирует эмоциональное состояние пользователя.
- **Использование Технологий**: В проекте используются ResNet для глубокого обучения, haarcascade для распознавания лиц на фотографиях, tg-bot для загрузки и отправки фотографии. 
- **Хранение Данных**: Результаты предсказаний модели (positive/negative) сохраняются в базе данных SQLite.

#### 2.2. Блок-схема решения  

  ![Блок-схема EmotionTracker](https://github.com/GarFang-MlOps/EmotionTracker/blob/main/docs/imgs/%D0%91%D0%BB%D0%BE%D0%BA%20%D1%81%D1%85%D0%B5%D0%BC%D0%B0%20EmotionTracker.PNG))

#### 2.3. Этапы решения задачи `Data Scientist`  

*Этап 1 - Подготовка данных.*  
  
| Название данных  | Есть ли данные в компании (если да, название источника/витрин) | Требуемый ресурс для получения данных (какие роли нужны) | Проверено ли качество данных (да, нет) |
| ------------- | ------------- | ------------- | ------------- |
| Изображения | Набор данных FER-2013 (Kaggle)  | DE/DS | + |
 
Результат этапа: Набор данных разделенный на тренировочную, тестовую и валидационную выборки, аннотирован для обучения модели.

*Этап 2: Подготовка прогнозных моделей*

*Бейзлайн:*

Модель: Простая модель основанная на архитектуре ResNet.
Результат: Базовая модель, способная классифицировать эмоции с умеренной точностью.

*MVP:*

Модель: Расширенная ResNet, оптимизированная для более сложных выражений лица.
Результат: Модель с высокой точностью классификации, способная распознавать более тонкие эмоциональные нюансы.

*Этап 3 - Метрики*

![metrics](https://github.com/GarFang-MlOps/EmotionTracker/blob/main/docs/imgs/metrics.PNG)

*Этап 4: Интеграция и тестирование*

Техника: Интеграция модели с кодом Telegram-бота, проведение тестов в реальных условиях.
Результат: Готовая к использованию система, способная анализировать эмоции по отправленным фотографиям пользователей.

*Этап 5: Мониторинг и оптимизация*

Техника: Сбор обратной связи от пользователей, анализ работы системы.
Результат: План по улучшению модели и системы на основе реального использования. 

### 3. Подготовка пилота

#### 3.1. Способ оценки пилота

- Дизайн оценки: Проведение A/B тестирования для сравнения производительности модели ResNet с бейзлайном. Это позволит оценить улучшения в точности и скорости работы модели.
- Участники: Реальные пользователи использующие наш сервис интегрированный с Telegram-бот.
- Критерии: Сравнение точности распознавания эмоций, скорости обработки запросов, и обратная связь пользователей.

#### 3.2. Что считаем успешным пилотом

- Метрики оценки успешности: 
   - Увеличение точности распознавания эмоций на 10% по сравнению с бейзлайном.
   - Сокращение времени обработки запроса на 5%.
   - Положительная обратная связь от не менее чем 70% пользователей.

#### 3.3. Подготовка пилота

- Оценка вычислительной сложности: На начальном этапе будет проведен эксперимент с бейзлайновой моделью для оценки требований к вычислительным ресурсам. Это даст понимание возможных ограничений и необходимых ресурсов для запуска усовершенствованной модели.
- Параметры пилота: После оценки вычислительной сложности бейзлайна, параметры пилота могут быть скорректированы для оптимизации производительности и затрат. Возможно, потребуется установление ограничений на сложность модели, чтобы обеспечить баланс между точностью и производительностью.

Подготовка пилота требует тщательного планирования и согласования между `Data Scientist` и `Product Owner` для обеспечения эффективного и целесообразного тестирования модели, а также для максимального соответствия бизнес-целям и ограничениям.

### 4. Внедрение 
  
#### 4.1. Архитектура решения   
  
| MLOps Components  | Tools |
| ------------- | ------------- |
| Data Science | Python, PyTorch, OpenCV, ResNet  |
| Source Control  | Git  |
| Experimentation  | JupyterLab  |
| Test & Build Services  | PyTest & Make  |
| Deployment Services  | Git  |
| Model & Dataset Registry  | Weights&Biases[s3]  |
| Feature Store  | SQLite  |
| ML Metadata Store  | Weights&Biases  |
| User Interface  | Telegram-bot  |
| Code Repository  | GitHub  |	
  
#### 4.2. Описание инфраструктуры и масштабируемости 

- Инфраструктура: Выбрана гибридная модель с использованием облачных ресурсов, что обеспечивает гибкость и масштабируемость решения.
- Плюсы: Гибкость в управлении ресурсами, масштабируемость под различные нагрузки, оптимизация затрат. Минусы: Стоимость.
- Выбор: Финальный выбор обеспечивает оптимальный баланс между производительностью, стоимостью и надежностью.
  
#### 4.3. Требования к работе системы  
  
- SLA: 99.9% доступности.
- Пропускная способность: Обработка до 1000 запросов в минуту.
- Задержка: Отклик системы не более 2 секунд.
  
#### 4.4. Безопасность системы  
  
- Потенциальные риски связаны с защитой конфиденциальности данных пользователей.
  
#### 4.5. Безопасность данных   
  
- Все пользовательские данные обрабатываются с соблюдением требований GDPR, а также других применимых норм и законов.
  
#### 4.6. Издержки  
  
- Расчетные издержки на работу системы на первоначальном этапе составляют около 200 долларов США в месяц, учитывая облачные сервисы, хранение данных и вычислительные ресурсы.
  
#### 4.5. Integration points  
  
- Взаимодействие сервисов: Интеграция между Telegram-ботом (API для взаимодействия с пользователями) и серверной частью (обработка запросов, предоставление результатов).
  
#### 4.6. Риски  
  
- Включают задержки в обработке запросов при высоких нагрузках, потенциальные сбои в системе безопасности, непредвиденные затраты на обслуживание и поддержку системы.  
