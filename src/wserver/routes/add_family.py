from flask import render_template, request, current_app, jsonify, redirect, url_for, g
from pprint import pformat
from .gwd import gwd_bp


@gwd_bp.route('/gwd/<base>/ADD_FAM/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/ADD_FAM/<lang>', methods=['GET', 'POST'])
def route_ADD_FAM(base, lang='en'):
    # Set the locale for this request based on URL path parameter
    g.locale = lang
    # Default number of children forms to show
    num_children = 1

    # If this is a form submission, capture the incoming data
    if request.method == 'POST':
        # Collect all form fields (including repeated names)
        form_data = request.form.to_dict(flat=False)
        files_info = {k: v.filename for k, v in request.files.items()}

        # Check if user clicked "Insert children" buttons
        is_insert = False
        if 'ins_ch0' in form_data:
            # User wants to insert children at position 0 (before first child)
            try:
                num_to_insert = int(request.form.get('ins_ch0_n', 1))
                num_children = num_to_insert + 1  # Add to existing first child
                is_insert = True
            except (ValueError, TypeError):
                num_children = 2
        elif 'ins_ch1' in form_data:
            # User wants to insert children after first child
            try:
                num_to_insert = int(request.form.get('ins_ch1_n', 1))
                num_children = 1 + num_to_insert
                is_insert = True
            except (ValueError, TypeError):
                num_children = 2

        # If it's an insert operation, re-render the form with more children
        if is_insert:
            return render_template(
                'gwd/add_family.html',
                base=base,
                lang=lang,
                num_children=num_children,
                form_data=request.form,
            )

        # Otherwise, it's a real submission
        try:
            current_app.logger.info(
                "ADD_FAM submitted for base=%s lang=%s: %d fields, %d files",
                base, lang, len(form_data), len(files_info)
            )
            # Also log keys for quick visibility
            current_app.logger.debug("Fields: %s", sorted(form_data.keys()))
            # Pretty-print full form contents and files for easier debugging
            current_app.logger.info(
                "ADD_FAM form fields:\n%s", pformat(form_data))
            current_app.logger.info("ADD_FAM files:\n%s", pformat(files_info))
        except Exception:
            # Fallback printing if current_app isn't available (prints to terminal)
            print("[ADD_FAM] form submitted:")
            try:
                print(pformat(form_data))
                print("Files:", pformat(files_info))
            except Exception:
                # Last-resort fallback
                print(list(form_data.keys()), files_info)

        # If the client asks JSON explicitly, return what we captured
        if request.accept_mimetypes.best == 'application/json':
            return jsonify({
                'ok': True,
                'base': base,
                'lang': lang,
                'fields': form_data,
                'files': files_info,
            })

        # Otherwise, use Post/Redirect/Get to avoid repost on browser reload.
        # Redirect back to the GET view and pass a small query flag so the
        # page can show a confirmation if desired.
        return redirect(
            url_for('gwd.route_ADD_FAM', base=base, lang=lang,
                    submitted=1, count=len(form_data))
        )

    # GET: render the form. If redirected after a POST, read the query
    # parameters to show a submission confirmation if needed.
    submitted = request.args.get('submitted') is not None
    submitted_count = request.args.get('count', default=0, type=int)
    return render_template(
        'gwd/add_family.html',
        base=base,
        lang=lang,
        submitted=submitted,
        submitted_count=submitted_count,
        num_children=num_children,
    )
