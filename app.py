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
        page_title="Arithmetic Sequence Generator",
        page_icon="🔢",
        layout="centered"
    )
    
    # Main title and description
    st.title("🔢 Arithmetic Sequence Generator")
    st.markdown("""
    Generate arithmetic sequences by specifying the first term, common difference, and number of terms.
    
    **Formula:** aₙ = a₁ + (n-1)d
    - a₁ = first term
    - d = common difference  
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
            help="The first number in your arithmetic sequence"
        )
    
    with col2:
        common_difference = st.number_input(
            "Common Difference (d)",
            value=1.0,
            step=1.0,
            help="The constant difference between consecutive terms"
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
        # Generate the arithmetic sequence
        try:
            sequence = generate_arithmetic_sequence(first_term, common_difference, int(num_terms))
            
            if sequence:
                # Display results section
                st.header("Generated Sequence")
                
                # Show sequence information
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("First Term", f"{first_term:.6g}")
                with col2:
                    st.metric("Common Difference", f"{common_difference:.6g}")
                with col3:
                    st.metric("Number of Terms", int(num_terms))
                
                # Display the sequence
                st.subheader("Sequence:")
                formatted_sequence = format_sequence_display(sequence)
                st.code(formatted_sequence, language=None)
                
                # Show additional information
                if len(sequence) > 1:
                    last_term = sequence[-1]
                    sequence_sum = sum(sequence)
                    
                    st.subheader("Additional Information:")
                    info_col1, info_col2 = st.columns(2)
                    
                    with info_col1:
                        st.info(f"**Last Term:** {last_term:.6g}")
                        st.info(f"**Sum of Sequence:** {sequence_sum:.6g}")
                    
                    with info_col2:
                        # Calculate range
                        sequence_range = max(sequence) - min(sequence)
                        st.info(f"**Range:** {sequence_range:.6g}")
                        
                        # Show formula for nth term
                        if common_difference >= 0:
                            formula = f"aₙ = {first_term:.6g} + (n-1) × {common_difference:.6g}"
                        else:
                            formula = f"aₙ = {first_term:.6g} - (n-1) × {abs(common_difference):.6g}"
                        st.info(f"**Formula:** {formula}")
                
                # Option to download as text file
                sequence_text = f"Arithmetic Sequence\n"
                sequence_text += f"First Term: {first_term:.6g}\n"
                sequence_text += f"Common Difference: {common_difference:.6g}\n"
                sequence_text += f"Number of Terms: {int(num_terms)}\n"
                sequence_text += f"Sequence: {formatted_sequence}\n"
                
                st.download_button(
                    label="📥 Download Sequence",
                    data=sequence_text,
                    file_name=f"arithmetic_sequence_{first_term}_{common_difference}_{num_terms}.txt",
                    mime="text/plain"
                )
            
        except Exception as e:
            st.error(f"❌ An error occurred while generating the sequence: {str(e)}")
    
    # Add some examples at the bottom
    with st.expander("📚 Examples"):
        st.markdown("""
        **Example 1:** Natural Numbers
        - First Term: 1, Common Difference: 1, Terms: 10
        - Result: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
        
        **Example 2:** Even Numbers
        - First Term: 2, Common Difference: 2, Terms: 8
        - Result: 2, 4, 6, 8, 10, 12, 14, 16
        
        **Example 3:** Decreasing Sequence
        - First Term: 100, Common Difference: -5, Terms: 6
        - Result: 100, 95, 90, 85, 80, 75
        
        **Example 4:** Decimal Sequence
        - First Term: 0.5, Common Difference: 0.25, Terms: 8
        - Result: 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.25
        """)

if __name__ == "__main__":
    main()
