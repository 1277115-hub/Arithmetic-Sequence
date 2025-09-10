import streamlit as st

def generate_arithmetic_sequence(first_term, common_difference, num_terms):
    """
    Generate an arithmetic sequence given first term, common difference, and number of terms.
    
    Args:
        first_term (float): The first term of the sequence
        common_difference (float): The common difference between consecutive terms
        num_terms (int): The number of terms to generate
    
    Returns:
        list: The arithmetic sequence as a list of numbers
    """
    if num_terms <= 0:
        return []
    
    sequence = []
    for i in range(num_terms):
        term = first_term + (i * common_difference)
        sequence.append(term)
    
    return sequence

def generate_geometric_sequence(first_term, common_ratio, num_terms):
    """
    Generate a geometric sequence given first term, common ratio, and number of terms.
    
    Args:
        first_term (float): The first term of the sequence
        common_ratio (float): The common ratio between consecutive terms
        num_terms (int): The number of terms to generate
    
    Returns:
        list: The geometric sequence as a list of numbers
    """
    if num_terms <= 0:
        return []
    
    sequence = []
    for i in range(num_terms):
        term = first_term * (common_ratio ** i)
        sequence.append(term)
    
    return sequence

def calculate_arithmetic_sum(first_term, common_difference, num_terms):
    """
    Calculate the sum of an arithmetic series using the formula: S_n = n/2 * (2a + (n-1)d)
    """
    if num_terms <= 0:
        return 0
    return num_terms / 2 * (2 * first_term + (num_terms - 1) * common_difference)

def calculate_geometric_sum(first_term, common_ratio, num_terms):
    """
    Calculate the sum of a geometric series using the formula:
    - If r = 1: S_n = n * a
    - If r ≠ 1: S_n = a * (1 - r^n) / (1 - r)
    """
    if num_terms <= 0:
        return 0
    
    if common_ratio == 1:
        return num_terms * first_term
    else:
        return first_term * (1 - common_ratio ** num_terms) / (1 - common_ratio)

def format_sequence_display(sequence):
    """
    Format the sequence for display with proper number formatting.
    
    Args:
        sequence (list): List of numbers in the sequence
    
    Returns:
        str: Formatted string representation of the sequence
    """
    if not sequence:
        return "No terms to display"
    
    # Format numbers to remove unnecessary decimal places
    formatted_terms = []
    for term in sequence:
        if term == int(term):
            formatted_terms.append(str(int(term)))
        else:
            formatted_terms.append(f"{term:.6g}")  # Use general format to avoid too many decimals
    
    return ", ".join(formatted_terms)

def main():
    # Set page configuration
    st.set_page_config(
        page_title="Sequence Generator",
        page_icon="🔢",
        layout="centered"
    )
    
    # Main title and description
    st.title("🔢 Sequence Generator")
    st.markdown("""
    Generate arithmetic or geometric sequences by specifying the parameters.
    """)
    
    # Sequence type selection
    sequence_type = st.radio(
        "Select Sequence Type:",
        ["Arithmetic", "Geometric"],
        horizontal=True,
        help="Choose between arithmetic or geometric sequence generation"
    )
    
    if sequence_type == "Arithmetic":
        st.markdown("""
        **Arithmetic Sequence Formula:** aₙ = a₁ + (n-1)d
        - a₁ = first term
        - d = common difference  
        - n = term position
        """)
    else:
        st.markdown("""
        **Geometric Sequence Formula:** aₙ = a₁ × rⁿ⁻¹
        - a₁ = first term
        - r = common ratio
        - n = term position
        """)
    
    # Create input section
    st.header("Input Parameters")
    
    # Create three columns for inputs
    col1, col2, col3 = st.columns(3)
    
    with col1:
        first_term = st.number_input(
            "First Term (a₁)",
            value=1.0,
            step=1.0,
            help=f"The first number in your {sequence_type.lower()} sequence"
        )
    
    with col2:
        if sequence_type == "Arithmetic":
            second_param = st.number_input(
                "Common Difference (d)",
                value=1.0,
                step=1.0,
                help="The constant difference between consecutive terms"
            )
        else:
            second_param = st.number_input(
                "Common Ratio (r)",
                value=2.0,
                step=0.1,
                help="The constant ratio between consecutive terms"
            )
    
    with col3:
        num_terms = st.number_input(
            "Number of Terms",
            min_value=1,
            max_value=1000,
            value=10,
            step=1,
            help="How many terms to generate (max 1000)"
        )
    
    # Input validation and error handling
    if num_terms > 1000:
        st.error("⚠️ Number of terms cannot exceed 1000 for performance reasons.")
        return
    
    if num_terms <= 0:
        st.error("⚠️ Number of terms must be a positive integer.")
        return
    
    # Generate sequence button (optional - could also auto-generate)
    if st.button("Generate Sequence", type="primary"):
        st.session_state.generate_clicked = True
    
    # Auto-generate on input change or if button was clicked
    if 'generate_clicked' not in st.session_state:
        st.session_state.generate_clicked = True
    
    if st.session_state.generate_clicked:
        try:
            # Generate the sequence based on type
            if sequence_type == "Arithmetic":
                sequence = generate_arithmetic_sequence(first_term, second_param, int(num_terms))
                calculated_sum = calculate_arithmetic_sum(first_term, second_param, int(num_terms))
            else:
                sequence = generate_geometric_sequence(first_term, second_param, int(num_terms))
                calculated_sum = calculate_geometric_sum(first_term, second_param, int(num_terms))
            
            if sequence:
                # Display results section
                st.header(f"Generated {sequence_type} Sequence")
                
                # Show sequence information
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("First Term", f"{first_term:.6g}")
                with col2:
                    if sequence_type == "Arithmetic":
                        st.metric("Common Difference", f"{second_param:.6g}")
                    else:
                        st.metric("Common Ratio", f"{second_param:.6g}")
                with col3:
                    st.metric("Number of Terms", int(num_terms))
                
                # Display the sequence
                st.subheader("Sequence:")
                formatted_sequence = format_sequence_display(sequence)
                st.code(formatted_sequence, language=None)
                
                # Show additional information
                if len(sequence) > 1:
                    last_term = sequence[-1]
                    actual_sum = sum(sequence)  # Direct sum for verification
                    
                    st.subheader("Additional Information:")
                    info_col1, info_col2 = st.columns(2)
                    
                    with info_col1:
                        st.info(f"**Last Term:** {last_term:.6g}")
                        st.info(f"**Sum of Series:** {calculated_sum:.6g}")
                        st.info(f"**Sum (Verification):** {actual_sum:.6g}")
                    
                    with info_col2:
                        # Calculate range
                        sequence_range = max(sequence) - min(sequence)
                        st.info(f"**Range:** {sequence_range:.6g}")
                        
                        # Show formula for nth term
                        if sequence_type == "Arithmetic":
                            if second_param >= 0:
                                formula = f"aₙ = {first_term:.6g} + (n-1) × {second_param:.6g}"
                            else:
                                formula = f"aₙ = {first_term:.6g} - (n-1) × {abs(second_param):.6g}"
                        else:
                            formula = f"aₙ = {first_term:.6g} × {second_param:.6g}ⁿ⁻¹"
                        st.info(f"**Formula:** {formula}")
                
                # Option to download as text file
                sequence_text = f"{sequence_type} Sequence\n"
                sequence_text += f"First Term: {first_term:.6g}\n"
                if sequence_type == "Arithmetic":
                    sequence_text += f"Common Difference: {second_param:.6g}\n"
                else:
                    sequence_text += f"Common Ratio: {second_param:.6g}\n"
                sequence_text += f"Number of Terms: {int(num_terms)}\n"
                sequence_text += f"Sequence: {formatted_sequence}\n"
                sequence_text += f"Sum of Series: {calculated_sum:.6g}\n"
                
                st.download_button(
                    label="📥 Download Sequence",
                    data=sequence_text,
                    file_name=f"{sequence_type.lower()}_sequence_{first_term}_{second_param}_{num_terms}.txt",
                    mime="text/plain"
                )
            
        except Exception as e:
            st.error(f"❌ An error occurred while generating the sequence: {str(e)}")
    
    # Add some examples at the bottom
    with st.expander("📚 Examples"):
        if sequence_type == "Arithmetic":
            st.markdown("""
            **Arithmetic Sequence Examples:**
            
            **Example 1:** Natural Numbers
            - First Term: 1, Common Difference: 1, Terms: 10
            - Result: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
            - Sum: 55
            
            **Example 2:** Even Numbers
            - First Term: 2, Common Difference: 2, Terms: 8
            - Result: 2, 4, 6, 8, 10, 12, 14, 16
            - Sum: 72
            
            **Example 3:** Decreasing Sequence
            - First Term: 100, Common Difference: -5, Terms: 6
            - Result: 100, 95, 90, 85, 80, 75
            - Sum: 525
            
            **Example 4:** Decimal Sequence
            - First Term: 0.5, Common Difference: 0.25, Terms: 8
            - Result: 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.25
            - Sum: 12
            """)
        else:
            st.markdown("""
            **Geometric Sequence Examples:**
            
            **Example 1:** Powers of 2
            - First Term: 1, Common Ratio: 2, Terms: 8
            - Result: 1, 2, 4, 8, 16, 32, 64, 128
            - Sum: 255
            
            **Example 2:** Powers of 3
            - First Term: 3, Common Ratio: 3, Terms: 5
            - Result: 3, 9, 27, 81, 243
            - Sum: 363
            
            **Example 3:** Decreasing Geometric
            - First Term: 100, Common Ratio: 0.5, Terms: 6
            - Result: 100, 50, 25, 12.5, 6.25, 3.125
            - Sum: 196.875
            
            **Example 4:** Decimal Ratio
            - First Term: 2, Common Ratio: 1.5, Terms: 6
            - Result: 2, 3, 4.5, 6.75, 10.125, 15.1875
            - Sum: 41.5625
            """)

if __name__ == "__main__":
    main()
