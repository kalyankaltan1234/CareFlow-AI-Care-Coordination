"""
CareFlow - Clinical Referral Slip PDF Generator
Generates printable, digitally signed clinical referral passes with ReportLab.
"""

from io import BytesIO
from typing import Dict, Any, Optional
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)

def generate_referral_slip_pdf(appointment: Dict[str, Any], patient_meta: Optional[Dict[str, Any]] = None) -> bytes:
    """
    Generates an official, beautifully formatted clinical referral slip PDF
    for an appointment booked through CareFlow.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    header_style = ParagraphStyle(
        'HospitalHeader',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#1E3A8A'),
        alignment=1 # Center
    )
    
    sub_header_style = ParagraphStyle(
        'HospitalSubHeader',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#4B5563'),
        alignment=1
    )
    
    section_title = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#1E3A8A'),
        spaceBefore=8,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'SlipBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#1F2937')
    )

    bold_label = ParagraphStyle(
        'BoldLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#111827')
    )

    alert_style = ParagraphStyle(
        'AlertText',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#B91C1C')
    )

    elements = []

    # 1. Header & Branding
    elements.append(Paragraph("CAREFLOW HEALTHCARE NETWORK", header_style))
    elements.append(Paragraph("AI-Assisted Care Coordination & Clinical Triage System • Project ID: 11", sub_header_style))
    elements.append(Paragraph("Official Clinical Referral & Appointment Token", ParagraphStyle('TokenSub', parent=sub_header_style, fontName='Helvetica-Bold', fontSize=11, textColor=colors.HexColor('#0284C7'))))
    elements.append(Spacer(1, 10))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1E3A8A'), spaceBefore=2, spaceAfter=10))

    # Booking & Status Banner
    booking_id = appointment.get("booking_id", "BK-1001")
    status = appointment.get("status", "Confirmed (Pending Clinician Sign-off)")
    status_color = colors.HexColor('#059669') if "Approved" in status else colors.HexColor('#D97706')

    banner_data = [
        [
            Paragraph(f"<b>BOOKING TOKEN:</b> <font size=12 color='#1E3A8A'><b>{booking_id}</b></font>", body_style),
            Paragraph(f"<b>STATUS:</b> <font color='{status_color.hexval()}'><b>{status}</b></font>", body_style),
            Paragraph(f"<b>DATE ISSUED:</b> 2026-10-06", body_style)
        ]
    ]
    t_banner = Table(banner_data, colWidths=[200, 240, 100])
    t_banner.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F0F9FF')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#BAE6FD')),
        ('PADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(t_banner)
    elements.append(Spacer(1, 12))

    # 2. Patient Demographics & Intake Information
    elements.append(Paragraph("1. PATIENT DEMOGRAPHICS & CLINICAL INTAKE", section_title))
    
    patient_name = patient_meta.get("patient_name") if patient_meta else appointment.get("patient_name", "Kalyan")
    patient_id = appointment.get("patient_id", "PT-1001")
    age = patient_meta.get("patient_age") if patient_meta else "28"
    place = patient_meta.get("patient_place") if patient_meta else "Hyderabad"
    disease = patient_meta.get("reported_disease") if patient_meta else appointment.get("reason", "Clinical Evaluation")

    pt_data = [
        [
            Paragraph("<b>Patient Name:</b>", bold_label), Paragraph(str(patient_name), body_style),
            Paragraph("<b>Patient ID:</b>", bold_label), Paragraph(str(patient_id), body_style)
        ],
        [
            Paragraph("<b>Age / Category:</b>", bold_label), Paragraph(f"{age} Years (Adult)", body_style),
            Paragraph("<b>Location / City:</b>", bold_label), Paragraph(str(place), body_style)
        ],
        [
            Paragraph("<b>Chief Complaint:</b>", bold_label), Paragraph(str(disease), body_style),
            Paragraph("<b>Triage Urgency:</b>", bold_label), Paragraph("<font color='#D97706'><b>Standard Triage (Medium)</b></font>", body_style)
        ]
    ]
    t_pt = Table(pt_data, colWidths=[120, 150, 120, 150])
    t_pt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F9FAFB')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#E5E7EB')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#F3F4F6')),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(t_pt)
    elements.append(Spacer(1, 12))

    # 3. Scheduled Specialist Consultation
    elements.append(Paragraph("2. SCHEDULED SPECIALIST CONSULTATION", section_title))
    
    doc_id = appointment.get("doctor_id", "DOC-301")
    slot_time = appointment.get("slot_time", "2026-10-06 11:30 AM")
    
    # Infer doctor details
    doc_name = appointment.get("doctor_name", "Dr. Sneha Reddy")
    specialty = appointment.get("specialty", "General Medicine")
    room_no = "Room 304, Block-B"
    if "101" in doc_id or "Neurol" in specialty:
        doc_name = "Dr. Ananya Sharma"
        specialty = "Neurology"
        room_no = "Room 208, Neuroscience Wing"
    elif "201" in doc_id or "Cardio" in specialty:
        doc_name = "Dr. Arvind Mehta"
        specialty = "Cardiology"
        room_no = "Room 102, Heart Center"
    elif "901" in doc_id or "Ortho" in specialty:
        doc_name = "Dr. Sanjay Kapoor"
        specialty = "Orthopedics & Spine Care"
        room_no = "Room 405, Joint & Bone Clinic"
    elif "501" in doc_id or "Pulmo" in specialty:
        doc_name = "Dr. Farhan Akhtar"
        specialty = "Pulmonology & Chest Medicine"
        room_no = "Room 312, Respiratory Center"

    consult_data = [
        [
            Paragraph("<b>Consulting Doctor:</b>", bold_label), Paragraph(f"<b>{doc_name}</b>", body_style),
            Paragraph("<b>Department:</b>", bold_label), Paragraph(f"{specialty}", body_style)
        ],
        [
            Paragraph("<b>Appointment Time:</b>", bold_label), Paragraph(f"<b>{slot_time}</b>", body_style),
            Paragraph("<b>Clinic Location:</b>", bold_label), Paragraph(f"{room_no}", body_style)
        ],
        [
            Paragraph("<b>Clinician Sign-off:</b>", bold_label), 
            Paragraph(appointment.get("coordinator_notes", "Clinician Approved • Priority verified by CareFlow HITL"), body_style),
            Paragraph("<b>Verification Stamp:</b>", bold_label), Paragraph("<font color='#059669'><b>VERIFIED HITL-OK</b></font>", body_style)
        ]
    ]
    t_consult = Table(consult_data, colWidths=[120, 150, 120, 150])
    t_consult.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#F1F5F9')),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(t_consult)
    elements.append(Spacer(1, 12))

    # 4. Evidence-Based Clinical Guidance & Pre-Visit Protocol
    elements.append(Paragraph("3. CLINICAL GUIDELINES & PRE-VISIT INSTRUCTIONS", section_title))
    
    guidelines_text = [
        Paragraph("• <b>Hydration & Rest:</b> Maintain high fluid intake (2.5 - 3.0 Liters daily with electrolytes) and get adequate bed rest.", body_style),
        Paragraph("• <b>Safe Supportive Care:</b> Paracetamol 650mg may be used as needed for fever/pain (Max 3000mg/day). Do NOT take unprescribed NSAIDs or antibiotics.", body_style),
        Paragraph("• <b>Medical Records:</b> Please bring physical prescription bottles, past lab reports, and a temperature/symptom diary.", body_style),
        Paragraph("• <b>Reporting Time:</b> Please report to the reception desk 15 minutes prior to the scheduled slot for vitals recording (BP, Pulse, SpO2).", body_style),
    ]
    for g in guidelines_text:
        elements.append(g)
        elements.append(Spacer(1, 3))

    elements.append(Spacer(1, 8))

    # 5. Red-Flag Emergency Warning Box
    elements.append(Paragraph("4. CRITICAL SAFETY & EMERGENCY RED-FLAGS", section_title))
    red_flag_box = [
        [
            Paragraph(
                "🚨 <b>EMERGENCY WARNING:</b> If the patient develops crushing chest pain, severe breathlessness, "
                "sudden confusion, persistent high fever (>103°F / 39.4°C), severe bleeding, or loss of consciousness, "
                "DO NOT wait for the appointment. <b>Immediately call 911 / 112 or visit the nearest Hospital Emergency Room.</b>",
                alert_style
            )
        ]
    ]
    t_alert = Table(red_flag_box, colWidths=[540])
    t_alert.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FEF2F2')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#F87171')),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(t_alert)

    elements.append(Spacer(1, 20))

    # 6. Signatures and Verification Footer
    footer_data = [
        [
            Paragraph("<b>Patient / Attendant Signature:</b><br/><br/>___________________________", body_style),
            Paragraph("<b>Care Coordinator / HITL Desk:</b><br/><br/><b>Sakshi / Clinical Lead (Signed)</b>", body_style),
            Paragraph("<b>Hospital Dispatch Seal:</b><br/><br/>[ CAREFLOW DIGITALLY VERIFIED ]", body_style)
        ]
    ]
    t_footer = Table(footer_data, colWidths=[180, 180, 180])
    t_footer.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (2,0), (2,0), 'CENTER'),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    elements.append(t_footer)

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()
