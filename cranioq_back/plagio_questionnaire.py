"""Run this script after the application is set up the create a first questionnaire template."""


def create_questionnaire(database='default'):

    from questionnaires.models import QuestionTemplate as QuT, QuestionnaireTemplate, QuestionCategory, QuestionType
    from users.models import Role

    # create all the categories
    cat_patient_demographics = QuestionCategory(name='Patient Demographics',
                                                description='Information about the patients demographics.')
    cat_patient_demographics.save(force_insert=True, using=database)
    cat_head_shape = QuestionCategory(name='Head Shape/Asymmetry',
                                      description='Questions about the head shape of the patient.')
    cat_head_shape.save(force_insert=True, using=database)
    cat_sleeping = QuestionCategory(name='Sleeping',
                                    description='Questions about the sleeping habits of the patient.')
    cat_sleeping.save(force_insert=True, using=database)
    cat_growth = QuestionCategory(name='Growth and Development',
                                  description='Questions about the growth and development of the patient.')
    cat_growth.save(force_insert=True, using=database)
    cat_mother_demographics = QuestionCategory(name='Mothers demographics',
                                               description='Questions about the genetic mother of the patient.')
    cat_mother_demographics.save(force_insert=True, using=database)
    cat_pregnancy = QuestionCategory(name='Pregnancy and labour',
                                     description='Questions about the pregnancy and labout.')
    cat_pregnancy.save(force_insert=True, using=database)
    cat_nutrition = QuestionCategory(name='Nutrition', description='Questions about the nutrition of the patient.')
    cat_nutrition.save(force_insert=True, using=database)
    cat_medical_history = QuestionCategory(name='Medical History',
                                           description='Questions about the patients medical history.')
    cat_medical_history.save(force_insert=True, using=database)
    cat_clinical_assessment = QuestionCategory(name='Clinical Assessment',
                                               description='Clinical assessment of the patient.')
    cat_clinical_assessment.save(force_insert=True, using=database)
    cat_classification_head = QuestionCategory(name='Classification of Head Shape',
                                               description='Classification of the patients head shape.')
    cat_classification_head.save(force_insert=True, using=database)

    # get the types
    free_text = QuestionType.objects.using(database).get(type='free_text')
    checkbox = QuestionType.objects.using(database).get(type='checkbox')
    radio = QuestionType.objects.using(database).get(type='radio')

    # get the roles
    parent = Role.objects.using(database).get(role='anon')
    gp = Role.objects.using(database).get(role='gp')

    # create the questions
    questions_list = [
        QuT(type=free_text, question='Patients date of birth.',
            category=cat_patient_demographics, role=parent),
        QuT(type=free_text, question='At what gestational age was the baby born?',
            description='Gestation is the period of time between conception and birth.',
            category=cat_patient_demographics, role=parent),
        QuT(type=free_text, question='When did you first seek guidance from a health professional for '
                                     'the abnormal head shape?',
            description='Patients age at time.', category=cat_patient_demographics, role=parent),
        QuT(type=radio, question='What is the patients sex?', answers=['male', 'female'],
            category=cat_patient_demographics, role=parent),
        QuT(type=free_text, question='What was the babies birth weight?', description='Please answer in kg.',
            category=cat_patient_demographics, role=parent),
        QuT(type=radio, question='What is the babies ethnic background?',
            answers=[
                'White British',
                'White Irish',
                'White other',
                'Mixed White and black Caribbean',
                'Mixed White and black African',
                'Mixed White and Asian',
                'Mixed other Asian Indian',
                'Asian Pakistani',
                'Asian Bangladeshi',
                'Asian other',
                'Black Caribbean',
                'Black African',
                'Black Other',
                'Chinese',
                'Any other',
                'I do not wish to disclose'
            ], category=cat_patient_demographics, role=parent),
        QuT(type=free_text, question='When was the abnormal head shape first noticed?',
            description='Was it at birth or later? Please specify at what age roughly.',
            category=cat_head_shape, role=parent),
        QuT(type=radio, question='Has the head shape/asymmetry changed since it was first noticed?',
            answers=['Yes, it improved', 'Yes, it worsened', 'No, it stayed the same'],
            category=cat_head_shape, role=parent),
        QuT(type=free_text, question='Please describe the head shape/asymmetry.', category=cat_head_shape, role=parent),
        QuT(type=radio, question='Does the baby have a preference looking to one side?',
            answers=['Yes, to the left', 'Yes, to the right', 'No'], category=cat_head_shape, role=parent),
        QuT(type=checkbox, question='On which side does the baby mostly sleep?',
            answers=['back', 'front', 'right side', 'left side'], category=cat_sleeping, role=parent),
        QuT(type=checkbox, question='Have any of the following interventions been tried?',
            answers=['positioning', 'pillows', 'physiotherapy', 'cranial moudling helmets',
                     'osteopathy', 'craniosacral therapy', 'other'], category=cat_sleeping, role=parent),
        QuT(type=free_text, question='When did the child first smile?',
            description='Leave empty if the milestone has not been reached yet.', category=cat_growth, role=parent),
        QuT(type=free_text, question='When did the child first move his eyes to watch you?',
            description='Leave empty if the milestone has not been reached yet.', category=cat_growth, role=parent),
        QuT(type=free_text, question='When did the child say his first recognisable word?',
            description='Leave empty if the milestone has not been reached yet.', category=cat_growth, role=parent),
        QuT(type=free_text, question='When did the child first sit up unsupported?',
            description='Leave empty if the milestone has not been reached yet.', category=cat_growth, role=parent),
        QuT(type=free_text, question='When did the child first roll over?',
            description='Leave empty if the milestone has not been reached yet.', category=cat_growth, role=parent),
        QuT(type=free_text, question='When did the child first start crawling or buttom shuffling?',
            description='Leave empty if the milestone has not been reached yet.', category=cat_growth, role=parent),
        QuT(type=free_text, question='When did the child first stand alone?',
            description='Leave empty if the milestone has not been reached yet.', category=cat_growth, role=parent),
        QuT(type=free_text, question='When did the child first stand alone?',
            description='Leave empty if the milestone has not been reached yet.', category=cat_growth, role=parent),
        QuT(type=free_text, question='When did the child first walk holding on?',
            description='Leave empty if the milestone has not been reached yet.', category=cat_growth, role=parent),
        QuT(type=free_text, question='When did the child first walk alone?',
            description='Leave empty if the milestone has not been reached yet.', category=cat_growth, role=parent),
        QuT(type=free_text, question='When was the mothers age when she became pregnant?',
            description='Please answer in years.', category=cat_mother_demographics, role=parent),
        QuT(type=free_text, question='What was the fathers age at the time of conception?',
            description='Please answer in years.', category=cat_mother_demographics, role=parent),
        QuT(type=free_text, question='How many times was the mother pregnant before?', category=cat_pregnancy,
            role=parent),
        QuT(type=free_text, question='How many times gave the mother birth reaching at least 37 weeks pregnancy?',
            category=cat_pregnancy, role=parent),
        QuT(type=free_text,
            question='How many times gave the mother birth with less than 37 weeks pregnancy (premature)?',
            category=cat_pregnancy, role=parent),
        QuT(type=free_text, question='How many times did the pregnancy end with an abortion?', category=cat_pregnancy,
            role=parent),
        QuT(type=free_text, question='How many pregnancies were successful?', category=cat_pregnancy, role=parent),
        QuT(type=free_text, question='How many multiple pregnancies did the mother have?',
            description='A multiple pregnancy is a pregnancy where the mother is pregnant with more than one fetus.',
            category=cat_pregnancy, role=parent),
        QuT(type=free_text, question='What was the mothers occupation during pregnancy?',
            category=cat_pregnancy, role=parent),
        QuT(type=free_text, question='What was the mothers sleeping position during pregnancy?',
            description='Please provide the sleeping position for each trimester of the pregnancy.',
            category=cat_pregnancy, role=parent),
        QuT(type=checkbox, question='Where there any complications during pregnancy?',
            answers=['Gestational diabetes', 'High blood pressure', 'Oligohydramnios', 'IVF', 'Multiple pregnancies',
                     'Breech position'], category=cat_pregnancy, role=parent),
        QuT(type=free_text, question='Where any supplements or medications taken during pregnancy? If yes which?',
            description='For example Folic Acid or Vitamin D?', category=cat_pregnancy, role=parent),
        QuT(type=free_text, question='Did the mother drink alcohol during pregnancy?',
            description='Please provide an answer for every trimester.', category=cat_pregnancy, role=parent),
        QuT(type=free_text, question='Does anyone in the household smoke? If yes who?',
            category=cat_pregnancy, role=parent),
        QuT(type=free_text, question='How long did it take for the baby to be born?',
            description='Time from first contraction to the delivery of the baby.',
            category=cat_pregnancy, role=parent),
        QuT(type=radio, question='How was the baby delivered?',
            answers=['Vaginal, bed delivery', 'Vaginal, water delivery', 'Vaginal, forceps assisted delivery',
                     'Vaginal, vacuum assisted delivery', 'Caesarean'], category=cat_pregnancy, role=parent),
        QuT(type=free_text, question='Where there any complications of labour? If yes please specify.',
            category=cat_pregnancy, role=parent),
        QuT(type=free_text, question='How long did the mother stay in hospital after delivery?',
            category=cat_pregnancy, role=parent),
        QuT(type=free_text, question='Was the baby admitted to NICU/HDU? If yes why and for how long?',
            category=cat_pregnancy, role=parent),
        QuT(type=radio, question='How is the baby fed?', answers=['Breast', 'Bottle', 'Combined'],
            category=cat_nutrition, role=parent),
        QuT(type=free_text, question='Has the baby started formula feed? If yes at what age?',
            category=cat_nutrition, role=parent),
        QuT(type=free_text, question='Does the baby has any other significant medical history?',
            category=cat_medical_history, role=parent),
        QuT(type=free_text, question='Does the baby has any other significant past surgical history?',
            category=cat_medical_history, role=parent),
        QuT(type=free_text, question='Does the baby have a preference to turn or rotate his/her head to one side?',
            description='If yes please please provide the side.', category=cat_clinical_assessment, role=parent),
        QuT(type=free_text, question='Does the baby have a head tilt? Which SCM is shorter?',
            category=cat_clinical_assessment, role=gp),
        QuT(type=free_text, question='Has the baby ever have a squint?', category=cat_clinical_assessment, role=parent),
        QuT(type=free_text, question='Please provide the head circumference.', category=cat_classification_head,
            role=gp),
        QuT(type=free_text, question='Please describe the general head shape.', description='Left/Right/Symmetric',
            category=cat_classification_head, role=gp),
        QuT(type=free_text, question='Please describe the ear position.',
            description='Relative to flattening - anterior or posterior', category=cat_classification_head, role=gp),
        QuT(type=free_text, question='Frontal bossing?',
            description='Right/Left/Symmetric', category=cat_classification_head, role=gp),
        QuT(type=free_text, question='Facial Scoliosis?',
            description='Chin to left or right?', category=cat_classification_head, role=gp),
        QuT(type=free_text, question='Nasal root deviation?',
            description='Left/Right/Central', category=cat_classification_head, role=gp),
        QuT(type=free_text, question='Please describe the eyebrow position.',
            description='Left/Right/Symmetric', category=cat_classification_head, role=gp),
        QuT(type=free_text, question='Mastoid bossing?',
            description='Left/Right', category=cat_classification_head, role=gp),
        QuT(type=free_text, question='Parietal bossing?',
            description='Left/Right/Symmetric', category=cat_classification_head, role=gp),
        QuT(type=free_text, question='Fontanelle examination - open or closed?',
            description='Anterior and Posterior', category=cat_classification_head, role=gp),
        QuT(type=free_text, question='Sutural examination',
            description='Metopic, sargittal, left coronal, right coronal, left lambdoid, right lambdoid',
            category=cat_classification_head, role=gp),
        QuT(type=free_text, question='Is imaging available? Please state the findings.',
            category=cat_classification_head, role=gp)
    ]

    for question in questions_list:
        question.save(force_insert=True, using=database)

    # create the template
    template = QuestionnaireTemplate(name='Plagiocephaly Questionnaire', version='1.0',
                                     description='Plagiocephaly Questionnaire')
    template.save(force_insert=True, using=database)
    for question in questions_list:
        template.questions.add(question)
