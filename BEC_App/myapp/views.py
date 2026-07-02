from django.shortcuts import render, redirect
from .forms import TheoryExaminationFormStep1, TheoryExaminationFormStep2, PracticalExaminationStep1Form, PracticalExaminationStep2Form
from .models import TheoryExamination, PracticalExamination
from decimal import Decimal


def theory_examination_step1(request):
    if request.method == 'POST':
        form = TheoryExaminationFormStep1(request.POST)
        if form.is_valid():
            # Store the cleaned data in session to use in step 2
            request.session['theory_step1_data'] = form.cleaned_data
            return redirect('theory_examination_step2')
    else:
        form = TheoryExaminationFormStep1()
    return render(request, 'theory_examination_step1.html', {'form': form})

def theory_examination_step2(request):
    step1_data = request.session.get('theory_step1_data')
    if not step1_data:
        # if no data from step 1, redirect back to step 1
        return redirect('theory_examination_step1')

    if request.method == 'POST':
        form = TheoryExaminationFormStep2(request.POST)
        if form.is_valid():
            # combine step1 and step2 data and save the model
            step2_data = form.cleaned_data
            combined_data = {**step1_data, **step2_data}
            TheoryExamination.objects.create(**combined_data)
            
            # Clear session data
            request.session.pop('theory_step1_data')
            
            return redirect('theory_examination_success')  # redirect somewhere after successful save
    else:
        form = TheoryExaminationFormStep2()
    return render(request, 'theory_examination_step2.html', {'form': form})


def theory_examination_success(request):
    return render(request, 'theory_examination_success.html')



def practical_examination_step1(request):
    if request.method == 'POST':
        form = PracticalExaminationStep1Form(request.POST)
        if form.is_valid():
            step1_data = form.cleaned_data

            # Convert Decimal fields to string for session storage
            for key, value in step1_data.items():
                if isinstance(value, Decimal):
                    step1_data[key] = str(value)

            request.session['practical_step1_data'] = step1_data
            return redirect('practical_examination_step2')
        else:
            # if form is invalid → re-render with errors
            return render(request, 'practical_examination_step1.html', {'form': form})

    else:  
        # GET request → show empty form
        form = PracticalExaminationStep1Form()
        return render(request, 'practical_examination_step1.html', {'form': form})



def practical_examination_step2(request):
    step1_data = request.session.get('practical_step1_data')
    if not step1_data:
        return redirect('practical_examination_step1')

    if request.method == 'POST':
        form = PracticalExaminationStep2Form(request.POST)
        if form.is_valid():
            data = {**step1_data, **form.cleaned_data}

            # Convert back string fields to proper types
            if "amount_of_batch" in data:
                data["amount_of_batch"] = Decimal(data["amount_of_batch"])

            if "no_of_days" in data:
                data["no_of_days"] = int(data["no_of_days"])

            if "batch_no" in data:
                data["batch_no"] = int(data["batch_no"])

            if "no_of_students" in data:
                data["no_of_students"] = int(data["no_of_students"])

            practical_exam = PracticalExamination(**data)
            practical_exam.save()

            request.session.pop('practical_step1_data')
            return redirect('practical_examination_success')
    else:
        form = PracticalExaminationStep2Form()
    return render(request, 'practical_examination_step2.html', {'form': form})


def practical_examination_success(request):
    return render(request, 'practical_examination_success.html')

def exam_choice(request):
    if request.method == "POST":
        exam_type = request.POST.get("exam_type")
        if exam_type == "theory":
            return redirect("theory_examination_step1")
        elif exam_type == "practical":
            return redirect("practical_examination_step1")
    return render(request, "exam_choice.html")

def view_records_choice(request):
    if request.method == "POST":
        exam_type = request.POST.get("exam_type")
        if exam_type == "theory":
            return redirect("view_theory_records")
        elif exam_type == "practical":
            return redirect("view_practical_records")
    return render(request, "view_records_choice.html")

def view_theory_records(request):
    records = TheoryExamination.objects.all()
    return render(request, "view_theory_records.html", {"records": records})

def view_practical_records(request):
    records = PracticalExamination.objects.all()
    return render(request, "view_practical_records.html", {"records": records})
