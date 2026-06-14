import os, urllib.request, sys
sys.path.insert(0, '.')
from app import create_app, db
from app.models.school import School, SchoolMedia, SchoolActivity, SchoolService, SchoolGrade
from app.models.notification import Notification
from app.models.user import User

app = create_app()

SAMPLE_IMAGES = [
    ('https://images.unsplash.com/photo-1571260899304-425eee4c7efc?q=80&w=600&auto=format&fit=crop', 'lab.jpg'),
    ('https://images.unsplash.com/photo-1503676260728-1c00da094a0b?q=80&w=600&auto=format&fit=crop', 'library.jpg'),
    ('https://images.unsplash.com/photo-1427504494785-3a9ca7044f45?q=80&w=600&auto=format&fit=crop', 'classroom.jpg'),
    ('https://images.unsplash.com/photo-1513364776144-60967b0f800f?q=80&w=600&auto=format&fit=crop', 'art.jpg'),
    ('https://images.unsplash.com/photo-1524178232363-1fb2b075b655?q=80&w=600&auto=format&fit=crop', 'graduation.jpg'),
    ('https://images.unsplash.com/photo-1543269865-cbf427effbad?q=80&w=600&auto=format&fit=crop', 'parents.jpg'),
    ('https://images.unsplash.com/photo-1580582932707-520aed937b7b?q=80&w=600&auto=format&fit=crop', 'sports.jpg'),
    ('https://images.unsplash.com/photo-1562774053-701939374585?q=80&w=600&auto=format&fit=crop', 'computer-lab.jpg'),
    ('https://images.unsplash.com/photo-1523050854058-8df90110c7f5?q=80&w=600&auto=format&fit=crop', 'students.jpg'),
    ('https://images.unsplash.com/photo-1509062522246-3755977927d7?q=80&w=600&auto=format&fit=crop', 'school-building.jpg'),
]

with app.app_context():
    media_dir = os.path.join(app.root_path, 'static', 'uploads', 'media')
    os.makedirs(media_dir, exist_ok=True)

    # Download images
    downloaded = {}
    for url, fname in SAMPLE_IMAGES:
        dest = os.path.join(media_dir, fname)
        if not os.path.exists(dest):
            try:
                print(f'Downloading {fname}...')
                urllib.request.urlretrieve(url, dest)
                downloaded[fname] = dest
            except Exception as e:
                print(f'  Failed: {e}')
        else:
            downloaded[fname] = dest

    schools = School.query.all()
    school_images = [
        'lab.jpg', 'library.jpg', 'classroom.jpg', 'art.jpg',
        'students.jpg', 'school-building.jpg', 'sports.jpg', 'computer-lab.jpg'
    ]
    school_videos = []

    for school in schools:
        existing_count = school.media.count()
        if existing_count > 0:
            print(f'{school.name}: already has {existing_count} media items, skipping')
            continue

        print(f'Adding media for {school.name}...')
        # Add 3-5 images per school
        import random
        random.seed(school.id)
        selected = random.sample(school_images, min(4, len(school_images)))
        for i, img_name in enumerate(selected):
            if img_name in downloaded:
                media = SchoolMedia(
                    school_id=school.id,
                    media_type='image',
                    filename=img_name,
                    original_name=img_name,
                    title=f'صورة {i+1} - {school.name}',
                    description=f'صورة من مرافق {school.name}',
                    status='approved',
                    is_featured=(i == 0),
                )
                db.session.add(media)

        # Add school activities
        if not school.activities.first():
            activities_data = [
                ('نادي البرمجة والروبوت', 'نادي متخصص لتعليم البرمجة والروبوتات للطلاب', 'bi-cpu'),
                ('الفريق الرياضي', 'فرق رياضية في كرة القدم والسباحة وكرة السلة', 'bi-trophy'),
                ('نادي القراءة', 'نادي لتشجيع القراءة وتطوير مهارات اللغة', 'bi-book'),
                ('المختبر العلمي', 'تجارب علمية مبتكرة في مختبرات مجهزة', 'bi-flask'),
            ]
            for title, desc, icon in activities_data:
                db.session.add(SchoolActivity(school_id=school.id, title=title, description=desc, icon=icon))

        # Add school services
        if not school.services.first():
            services_data = [
                ('مكتبة رقمية', 'مكتبة إلكترونية تضم آلاف الكتب والمراجع', 'bi-book'),
                ('مقصف صحي', 'مقصف يقدم وجبات صحية ومتوازنة للطلاب', 'bi-cup-hot'),
                ('مواصلات مدرسية', 'خدمة توصيل آمنة ومريحة للطلاب', 'bi-bus-front'),
                ('رعاية صحية', 'عيادة طبية متكاملة مع طبيب مقيم', 'bi-heart-pulse'),
            ]
            for title, desc, icon in services_data:
                db.session.add(SchoolService(school_id=school.id, title=title, description=desc, icon=icon))

        # Add school grades
        if not school.grades.first():
            grades_data = [
                ('رياض أطفال', 'Kindergarten'),
                ('المرحلة الابتدائية', 'Primary'),
                ('المرحلة المتوسطة', 'Middle School'),
                ('المرحلة الثانوية', 'High School'),
            ]
            for name, name_en in grades_data:
                db.session.add(SchoolGrade(school_id=school.id, name=name, name_en=name_en))

    db.session.commit()
    print('Media, activities, services, and grades seeded successfully!')

    # Also check contact form notifications
    print(f'\nTotal notifications in DB: {Notification.query.count()}')
    print(f'Total admin users: {User.query.filter_by(role="admin").count()}')
