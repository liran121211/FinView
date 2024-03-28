import base64
import binascii
import io
import json
import os
import time

from PIL import Image
from datetime import datetime
from random import randint
from typing import Text, Any, List
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, FieldError, ObjectDoesNotExist, PermissionDenied
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import UploadedFile
from django.db import IntegrityError, DataError, DatabaseError
from django.db.models import ProtectedError
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404

from FinWeb.FinWebApp import Logger, FILE_UPLOAD_ERROR, FILE_SIZE_TOO_BIG, FILE_WRONG_TYPE, FILE_VALIDATION_ERROR, \
    FILE_UPLOAD_SUCCESS, FIN_CORE, FILE_WRONG_STRUCTURE, FIRST_IDX
from FinWeb.FinWebApp.models import UserFinancialInformation, UserCards, UserDirectDebitSubscriptions, \
    UserBankTransactions, \
    SpentByCategoryQuery, SpentByCardNumberQuery, IncomeByMonthQuery, UserCreditCardsTransactions, IncomeAgainstOutcome, \
    BankTransactionByCategoryQuery, UserPersonalInformation, SpentByMonthQuery


def home_view(request):
    if request.user.is_authenticated:
        logged_in_user = request.user.username

        return render(request, 'home.html', {
            'user_information': retrieve_user_information(logged_in_user),
            'user_cards': retrieve_user_cards(logged_in_user),
            'user_direct_debit_subscriptions': retrieve_user_direct_debit_subscription_records(logged_in_user),
            'user_income': slice_dictionary(retrieve_user_bank_transactions(logged_in_user, True), -5, 0),
            'user_outcome': slice_dictionary(retrieve_user_credit_card_transactions(logged_in_user), -5, 0),
            'spent_by_category': SpentByCategoryQuery(logged_in_user),  # Pie-Chart view
            'bank_transaction_by_category': BankTransactionByCategoryQuery(logged_in_user),  # Pie-Chart view
            'spent_by_card': SpentByCardNumberQuery(logged_in_user),  # Pie-Chart view
            'income_by_month': IncomeByMonthQuery(logged_in_user),
            'income_against_outcome': IncomeAgainstOutcome(logged_in_user),
            'avatar_title': "!" + "ברוך הבא, " + retrieve_user_personal_information(logged_in_user)['first_name']
        })
    else:
        return render(request, 'login.html', {'failure_login': 'אנא התחבר לפני הגישה לעמוד המבוקש'})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home_page')
    return render(request, 'login.html', )


def logout_view(request):
    logout(request)
    # Redirect to a specific page after logout
    return redirect('login_page')


def login_post(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home_page')
        else:
            return render(request, 'login.html', {'failure_login': 'שם משתמש או/ו סיסמא שגויים'})


def register_post(request):
    if request.user.is_authenticated:
        return redirect('home_page')
    else:
        if request.method == 'POST':
            try:
                full_name = request.POST['full_name'].split()
                User.objects.create_user(username=request.POST['username'],
                                         password=request.POST['password'],
                                         email=request.POST['email'],
                                         first_name=full_name[0],
                                         last_name=full_name[1],
                                         )

            except IntegrityError as e:
                # Handle field-related errors
                Logger.logger.critical(e)
                return render(request, 'login.html', {'failure_registration': 'הרישום נכשל, אנא נסה שוב'})
            except ValidationError as e:
                # Handle validation errors
                Logger.logger.critical(e)
                return render(request, 'login.html', {'failure_registration': 'הרישום נכשל, אנא נסה שוב'})
            except DatabaseError as e:
                # Handle database-related errors
                Logger.logger.critical(e)
                return render(request, 'login.html', {'failure_registration': 'הרישום נכשל, אנא נסה שוב'})
            except KeyError as e:
                # Handle dictionary errors
                Logger.logger.critical(e)
                return render(request, 'login.html', {'failure_registration': 'הרישום נכשל, אנא נסה שוב'})
            except IndexError as e:
                # Handle out of bound errors
                Logger.logger.critical(e)
                return render(request, 'login.html', {'failure_registration': 'הרישום נכשל, אנא נסה שוב'})
            except Exception as e:
                # Handle other unexpected exceptions
                Logger.logger.critical(e)
                return render(request, 'login.html', {'failure_registration': 'הרישום נכשל, אנא נסה שוב'})

            return render(request, 'login.html', {'success_registration': 'הרישום בוצע בהצלחה'})

        return redirect('login_page')


def analytics_and_trends_view(request):
    if request.user.is_authenticated:
        logged_in_user = request.user.username

        return render(request, 'analytics_and_trends.html', {
            'user_information': retrieve_user_information(logged_in_user),
            'spent_by_month_monthly': SpentByMonthQuery(dates=get_last_12_months(), username=logged_in_user, sort='Monthly'),
            'spent_by_month_quarterly': SpentByMonthQuery(dates=get_last_12_months(), username=logged_in_user, sort='Quarterly'),
            'spent_by_month_yearly': SpentByMonthQuery(dates=get_last_12_months(), username=logged_in_user, sort='Yearly')
        })
    else:
        return render(request, 'login.html', {'failure_login': 'אנא התחבר לפני הגישה לעמוד המבוקש'})


def settings_view(request):
    if request.user.is_authenticated:
        logged_in_user = request.user.username

        # handle personal information editing
        try:
            # Retrieve user from the database
            user_personal_information_object = get_object_or_404(UserPersonalInformation, pk=request.user.id)
            user_personal_information_object.active_user = 'פעיל' if user_personal_information_object.active_user is True else 'לא פעיל'
        except Http404 as e:
            Logger.logger.critical(e)
            raise Http404("This page does not exist")

        return render(request, 'settings.html', {
            'user_personal_information_instance': user_personal_information_object,
            'user_cards': retrieve_user_cards(logged_in_user),
            'credit_cards_transactions': retrieve_user_credit_card_transactions(logged_in_user),
            'bank_transactions': retrieve_user_bank_transactions(logged_in_user, positive_only=False),
            'direct_debit_subscriptions': retrieve_user_direct_debit_subscription_records(logged_in_user),
            'full_name': f"{request.user.first_name} {request.user.last_name}",
            'account_status': "משתמש פעיל" if request.user.is_active == True else "משתמש לא פעיל",
            'portrait': retrieve_user_personal_information(logged_in_user)['portrait']
        })

    return render(request, 'login.html', {'failure_login': 'אנא התחבר לפני הגישה לעמוד המבוקש'})


def settings_personal_information_post(request):
    # handle personal information editing
    try:
        # Retrieve user from the database
        user_personal_information_object = get_object_or_404(UserPersonalInformation, pk=request.user.id)
    except Http404 as e:
        Logger.logger.critical(e)
        raise Http404("This page does not exist")

    try:
        if request.content_type == 'application/json':
            # JSON decoding exception
            try:
                image_data = json.loads(request.body).get('image_data', None)
            except json.JSONDecodeError as e:
                Logger.critical(e)
                # Handle the JSON decoding error
            else:
                if image_data is not None:
                    # Decode base64-encoded image data
                    try:
                        # Remove the 'data:image/png;base64,' prefix
                        format, imgstr = image_data.split(';base64,')
                        # Decode base64 data
                        image_binary_data = base64.b64decode(imgstr)

                    except binascii.Error as e:
                        Logger.critical("Base64 decoding error:", e)
                        # Handle the Base64 decoding error
                    else:
                        # File operations exceptions
                        try:
                            # Create a file path for saving the image
                            local_image_path = os.path.join(settings.STATIC_ROOT, 'images', 'portraits', f"{request.user.username}_portrait.png")
                            global_image_path = os.path.join(settings.BASE_DIR, 'FinWebApp', 'static', 'images', 'portraits',f"{request.user.username}_portrait.png")

                            # Create a PIL Image object from the original image data
                            original_image = Image.open(io.BytesIO(image_binary_data))

                            # Convert the image format to PNG
                            converted_image = original_image.convert('RGB')  # Convert to RGB mode if necessary
                            converted_image.save(local_image_path, format='PNG')
                            converted_image.save(global_image_path, format='PNG')

                        except IOError as e:
                            Logger.critical("File operation error:", e)
                            # Handle the file operation error
    except Exception as e:
        Logger.critical("An unexpected error occurred while changing portrait picture:", e)
        # Handle any other unexpected errors

    user_personal_information_object.portrait = f"{request.user.username}_portrait.png"
    handle_instance_modification(user_personal_information_object)

    if request.method == 'POST':
        user_personal_information_object.first_name = request.POST.get('first_name',user_personal_information_object.first_name)
        user_personal_information_object.last_name = request.POST.get('last_name',user_personal_information_object.last_name)
        user_personal_information_object.email = request.POST.get('email', user_personal_information_object.email)
        user_personal_information_object.password = request.POST.get('password',user_personal_information_object.password)

        # check if modification of instance cause an exception
        if handle_instance_modification(user_personal_information_object):
            return redirect('settings_page')
    else:
        return redirect('settings_page')


def settings_user_cards_post(request):
    # handle credit cards editing
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            current_user_credit_cards_instance = get_object_or_404(UserCards, pk=request.POST.get('sha1_identifier'))  # Retrieve credit cards from the database  # Retrieve user from the database
        except Http404 as e:
            Logger.logger.critical(e)
            raise Http404("This page does not exist")

        # perform database update operation here
        current_user_credit_cards_instance.card_type = request.POST.get('selected_card_type', current_user_credit_cards_instance.card_type)

        # check if modification instance can cause an exception
        if handle_instance_modification(current_user_credit_cards_instance):
            return JsonResponse({'success': True})

        return JsonResponse({'success': False})

    else:
        return redirect('settings_page')


def retrieve_user_information(username: Text) -> dict:
    # Retrieve all rows from the table
    filtered_data = UserFinancialInformation.objects.filter(username=username).first()

    # if query was invalid or empty.
    if filtered_data is None:
        filtered_data = {
            'latest_debit': 0.0,
            'current_debit': 0.0,
            'total_saving': 0.0
        }
        return filtered_data

    return {
        'latest_debit': filtered_data.latest_debit,
        'current_debit': filtered_data.current_debit,
        'total_saving': filtered_data.total_saving,
    }


def retrieve_user_cards(username: Text) -> dict:
    # Retrieve all rows from the table
    filtered_data = UserCards.objects.filter(username=username).all()

    # if query was invalid or empty.
    if filtered_data is None:
        filtered_data = {
            'issuer_name': [],
            'last_4_digits': [],
            'card_type': [],
            'full_name': [],
            'sha1_identifier': [],
        }
        return filtered_data

    dict_data = dict()
    for data in filtered_data:
        if dict_data.get('issuer_name', None) is None:
            dict_data['issuer_name'] = [data.issuer_name]
        else:
            dict_data['issuer_name'].append(data.issuer_name)

        if dict_data.get('last_4_digits', None) is None:
            dict_data['last_4_digits'] = [data.last_4_digits]
        else:
            dict_data['last_4_digits'].append(data.last_4_digits)

        if dict_data.get('card_type', None) is None:
            dict_data['card_type'] = [data.card_type]
        else:
            dict_data['card_type'].append(data.card_type)

        if dict_data.get('full_name', None) is None:
            dict_data['full_name'] = [data.full_name]
        else:
            dict_data['full_name'].append(data.full_name)

        if dict_data.get('sha1_identifier', None) is None:
            dict_data['sha1_identifier'] = [data.sha1_identifier]
        else:
            dict_data['sha1_identifier'].append(data.sha1_identifier)

    return dict_data


def retrieve_user_direct_debit_subscription_records(username: Text) -> dict:
    # Retrieve all rows from the table
    filtered_data = UserDirectDebitSubscriptions.objects.filter(username=username).all()

    # if query was invalid or empty.
    if filtered_data is None:
        filtered_data = {
            'payment_type': [],
            'amount': [],
            'provider_name': [],
        }
        return filtered_data

    dict_data = dict()
    for data in filtered_data:
        if dict_data.get('payment_type', None) is None:
            dict_data['payment_type'] = [data.payment_type]
        else:
            dict_data['payment_type'].append(data.payment_type)

        if dict_data.get('amount', None) is None:
            dict_data['amount'] = [data.amount]
        else:
            dict_data['amount'].append(data.amount)

        if dict_data.get('provider_name', None) is None:
            dict_data['provider_name'] = [data.provider_name]
        else:
            dict_data['provider_name'].append(data.provider_name)

    return dict_data


def retrieve_user_credit_card_transactions(username: Text) -> dict:
    # Retrieve all rows from the table
    filtered_data = UserCreditCardsTransactions.objects.filter(username=username).order_by('-date_of_transaction')

    # if query was invalid or empty.
    if filtered_data is None:
        filtered_data = {
            'sha1_identifier': [],
            'date_of_transaction': [],
            'business_name': [],
            'charge_amount': [],
            'total_amount': [],
            'username': [],
            'transaction_provider': [],
            'transaction_type': [],
            'transaction_category': [],
            'last_4_digits': [],
        }
        return filtered_data

    dict_data = dict()
    for data in filtered_data:
        if dict_data.get('sha1_identifier', None) is None:
            dict_data['sha1_identifier'] = [data.sha1_identifier]
        else:
            dict_data['sha1_identifier'].append(data.sha1_identifier)

        if dict_data.get('date_of_transaction', None) is None:
            dict_data['date_of_transaction'] = [str(data.date_of_transaction)]
        else:
            dict_data['date_of_transaction'].append(str(data.date_of_transaction))

        if dict_data.get('business_name', None) is None:
            dict_data['business_name'] = [data.business_name]
        else:
            dict_data['business_name'].append(data.business_name)

        if dict_data.get('charge_amount', None) is None:
            dict_data['charge_amount'] = [data.charge_amount]
        else:
            dict_data['charge_amount'].append(data.charge_amount)

        if dict_data.get('total_amount', None) is None:
            dict_data['total_amount'] = [data.total_amount]
        else:
            dict_data['total_amount'].append(data.total_amount)

        if dict_data.get('username', None) is None:
            dict_data['username'] = [data.username]
        else:
            dict_data['username'].append(data.username)

        if dict_data.get('transaction_provider', None) is None:
            dict_data['transaction_provider'] = [data.transaction_provider]
        else:
            dict_data['transaction_provider'].append(data.transaction_provider)

        if dict_data.get('transaction_type', None) is None:
            dict_data['transaction_type'] = [data.transaction_type]
        else:
            dict_data['transaction_type'].append(data.transaction_type)

        if dict_data.get('transaction_category', None) is None:
            dict_data['transaction_category'] = [data.transaction_category]
        else:
            dict_data['transaction_category'].append(data.transaction_category)

        if dict_data.get('last_4_digits', None) is None:
            dict_data['last_4_digits'] = [data.last_4_digits]
        else:
            dict_data['last_4_digits'].append(data.last_4_digits)

    return dict_data


def retrieve_user_bank_transactions(username: Text, positive_only: bool) -> dict:
    if positive_only:
        filtered_data = UserBankTransactions.objects.filter(username=username, income_balance__gt=0).order_by('-transaction_date')
    else:
        # Retrieve all rows from the table
        filtered_data = UserBankTransactions.objects.filter(username=username).order_by('-transaction_date')

    # if query was invalid or empty.
    if filtered_data is None:
        filtered_data = {
            'sha1_identifier': [],
            'transaction_date': [],
            'transaction_description': [],
            'income_balance': [],
            'outcome_balance': [],
            'current_balance': [],
            'username': [],
            'transaction_provider': [],
            'account_number': [],
            'transaction_reference': [],
            'transaction_category': [],
        }
        return filtered_data

    dict_data = dict()
    for data in filtered_data:
        if dict_data.get('sha1_identifier', None) is None:
            dict_data['sha1_identifier'] = [data.sha1_identifier]
        else:
            dict_data['sha1_identifier'].append(data.sha1_identifier)

        if dict_data.get('transaction_date', None) is None:
            dict_data['transaction_date'] = [str(data.transaction_date)]
        else:
            dict_data['transaction_date'].append(str(data.transaction_date))

        if dict_data.get('transaction_description', None) is None:
            dict_data['transaction_description'] = [data.transaction_description]
        else:
            dict_data['transaction_description'].append(data.transaction_description)

        if dict_data.get('income_balance', None) is None:
            dict_data['income_balance'] = [data.income_balance]
        else:
            dict_data['income_balance'].append(data.income_balance)

        if dict_data.get('outcome_balance', None) is None:
            dict_data['outcome_balance'] = [data.outcome_balance]
        else:
            dict_data['outcome_balance'].append(data.outcome_balance)

        if dict_data.get('current_balance', None) is None:
            dict_data['current_balance'] = [data.current_balance]
        else:
            dict_data['current_balance'].append(data.current_balance)

        if dict_data.get('username', None) is None:
            dict_data['username'] = [data.username]
        else:
            dict_data['username'].append(data.username)

        if dict_data.get('transaction_provider', None) is None:
            dict_data['transaction_provider'] = [data.transaction_provider]
        else:
            dict_data['transaction_provider'].append(data.transaction_provider)

        if dict_data.get('account_number', None) is None:
            dict_data['account_number'] = [data.account_number]
        else:
            dict_data['account_number'].append(data.account_number)

        if dict_data.get('transaction_reference', None) is None:
            dict_data['transaction_reference'] = [data.transaction_reference]
        else:
            dict_data['transaction_reference'].append(data.transaction_reference)

        if dict_data.get('transaction_category', None) is None:
            dict_data['transaction_category'] = [data.transaction_category]
        else:
            dict_data['transaction_category'].append(data.transaction_category)

    return dict_data


def retrieve_user_personal_information(username: Text) -> dict:
    filtered_data = UserPersonalInformation.objects.filter(username=username).first()

    # if query was invalid or empty.
    if filtered_data is None:
        filtered_data = {
            'username': 'N/A',
            'first_name': 'N/A',
            'last_name': 'N/A',
            'email': 'N/A',
            'date_joined': 'N/A',
            'active_user': 'N/A',
            'portrait': 'N/A',
        }
        return filtered_data

    dict_data = dict()
    if dict_data.get('username', None) is None:
        dict_data['username'] = filtered_data.username
    else:
        dict_data['username'].append(filtered_data.username)

    if dict_data.get('first_name', None) is None:
        dict_data['first_name'] = filtered_data.first_name
    else:
        dict_data['first_name'].append(filtered_data.first_name)

    if dict_data.get('last_name', None) is None:
        dict_data['last_name'] = filtered_data.last_name
    else:
        dict_data['last_name'].append(filtered_data.last_name)

    if dict_data.get('email', None) is None:
        dict_data['email'] = filtered_data.email
    else:
        dict_data['email'].append(filtered_data.email)

    if dict_data.get('date_joined', None) is None:
        dict_data['date_joined'] = filtered_data.date_joined
    else:
        dict_data['date_joined'].append(filtered_data.date_joined)

    if dict_data.get('active_user', None) is None:
        dict_data['active_user'] = filtered_data.active_user
    else:
        dict_data['active_user'].append(filtered_data.active_user)

    if dict_data.get('portrait', None) is None:
        dict_data['portrait'] = filtered_data.portrait
    else:
        dict_data['portrait'].append(filtered_data.portrait)

    return dict_data


def slice_dictionary(obj: dict, start_idx: int = 0, end_idx: int = -1) -> dict:
    temp_dict = dict()
    matched_indexes = [i for i in range(len(obj.items()))]

    if not start_idx > len(matched_indexes) or not end_idx > len(matched_indexes):
        # if end index is not defined.
        if end_idx == 0:
            matched_indexes = matched_indexes[start_idx:]
        else:
            matched_indexes = matched_indexes[start_idx:end_idx]

    for k, v in obj.items():
        for i, value in enumerate(v):
            if i in matched_indexes:
                if k not in temp_dict.keys():
                    temp_dict[k] = [value]
                else:
                    temp_dict[k].append(value)

    return temp_dict


def get_last_12_months() -> List[List]:
    # Get the current date
    current_date = datetime.now()

    # List to store month/year strings
    months_list = [[current_date.strftime('%m'), current_date.strftime('%Y')]]

    # Iterate over the last 11 months
    for i in range(0, 11):
        # Subtract i months from the current date
        month_year = current_date - timedelta(days=current_date.day)
        month_year = month_year.replace(day=1)
        month_year -= timedelta(days=30.5 * i)  # Approximate months
        months_list.append([month_year.strftime('%m'), month_year.strftime('%Y')])

    return months_list


def handle_instance_modification(instance: Any) -> bool:
    try:
        instance.save()
        return True

    except IntegrityError as e:
        # Handle database integrity errors
        Logger.logger.critical(e)
        return False
    except ValidationError as e:
        # Handle validation errors
        Logger.logger.critical(e)
        return False
    except ObjectDoesNotExist as e:
        # Handle object not found errors
        Logger.logger.critical(e)
        return False
    except FieldError as e:
        # Handle field-related errors
        Logger.logger.critical(e)
        return False
    except DataError as e:
        # Handle data-related errors
        Logger.logger.critical(e)
        return False
    except Exception as e:
        # Handle other unexpected exceptions
        Logger.logger.critical(e)
        return False


def handle_instance_deletion(instance: Any) -> bool:
    try:
        instance.delete()
        return True

    except ObjectDoesNotExist as e:
        # Handle database integrity errors
        Logger.logger.critical(e)
        return False
    except ProtectedError as e:
        # Handle validation errors
        Logger.logger.critical(e)
        return False
    except PermissionDenied as e:
        # Handle object not found errors
        Logger.logger.critical(e)
        return False
    except IntegrityError as e:
        # Handle field-related errors
        Logger.logger.critical(e)
        return False
    except Exception as e:
        # Handle other unexpected exceptions
        Logger.logger.critical(e)
        return False


def handle_uploaded_file(file: UploadedFile, username: Text) -> int:
    """
    Function to handle uploaded securely.
    """

    try:
        for file_name in os.listdir(os.path.join(settings.MEDIA_ROOT, username)):
            file_path = os.path.join(os.path.join(settings.MEDIA_ROOT, username), file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
    except Exception as e:
        Logger.critical(e)

    try:
        # Validate file size
        if file.size > settings.MAX_UPLOAD_SIZE:
            Logger.warning("ValidationError: File size exceeds the allowed limit")
            return FILE_SIZE_TOO_BIG

        # Validate file type
        allowed_types = settings.ALLOWED_UPLOAD_TYPES
        if not file.content_type in allowed_types:
            Logger.warning("ValidationError: File type not allowed")
            return FILE_WRONG_TYPE

        # Generate a unique filename
        filename = str(username) + '_' + datetime.now().strftime("%d_%m_%y_%H_%M_%S") + '___' + file.name
        while os.path.exists(os.path.join(settings.MEDIA_ROOT, filename)):
            filename = str(username) + '_' + datetime.now().strftime("%d_%m_%y_%H_%M_%S") + '___'  + filename + '_' + randint(1, 100)

        # Save the file to the media directory
        try:
            if not os.path.exists(os.path.join(settings.MEDIA_ROOT, username)):
                os.makedirs(os.path.join(settings.MEDIA_ROOT, username))
                Logger.info(f"upload folder for user {username} has been created successfully.")
        except OSError:
            Logger.critical(f"creating upload folder for user {username} raised OSError.")

        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, username))
        _ = fs.save(filename, file)
        return FILE_UPLOAD_SUCCESS

    except ValidationError as e:
        # Handle validation errors
        Logger.warning(e)
        return FILE_VALIDATION_ERROR

    except Exception as e:
        Logger.warning(e)
        return FILE_UPLOAD_ERROR


def handle_processed_file(file: UploadedFile, username: Text) -> Any:
    result = FIN_CORE.load_statements_to_db(username, folder_path=os.path.join(settings.MEDIA_ROOT, username))

    if len(result) == 0:
        return FILE_WRONG_STRUCTURE
    return result




def upload_post(request):
    if request.user.is_authenticated:
        logged_in_user = request.user.username

        if request.method == 'POST' and request.FILES:
            file = request.FILES['upload-file-input']

            # process the uploaded file
            upload_status = handle_uploaded_file(file, logged_in_user)
            process_status = handle_processed_file(file, logged_in_user)

            if upload_status == FILE_WRONG_TYPE:
                return JsonResponse({'statusText': 'סוג קובץ אינו נתמך'}, status=FILE_WRONG_TYPE)

            if upload_status == FILE_SIZE_TOO_BIG:
                return JsonResponse({'statusText': 'גודל הקובץ חורג מ 10MB'}, status=FILE_SIZE_TOO_BIG)

            if upload_status == FILE_VALIDATION_ERROR:
                return JsonResponse({'statusText': 'קובץ אינו תקין'}, status=FILE_VALIDATION_ERROR)

            if process_status == FILE_WRONG_STRUCTURE:
                return JsonResponse({'statusText': 'הקובץ אינו במבנה תקין'}, status=FILE_WRONG_STRUCTURE)

            if upload_status == FILE_UPLOAD_SUCCESS:
                return JsonResponse({'statusText': 'הקובץ הועלה בהצלחה','Statistics': process_status}, status=FILE_UPLOAD_SUCCESS)

        return JsonResponse({'statusText': 'שגיאת העלאה כללית'}, status=FILE_UPLOAD_ERROR)


def handler404(request, exception):
    # Handle the 404 error and render the custom 404 template
    return render(request, '404.html', status=404)