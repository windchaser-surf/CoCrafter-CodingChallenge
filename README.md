# Coding Challenge - Folder & Document API

To start the containers, you can use the following command:

```bash
make up

## How long it took you to solve this?

- It took me approximately 10 hours to solve the task. During this time, I not only focused on implementing the solution but also deepened my knowledge of best practices in REST API design and design patterns. The research and study of these topics helped me develop a robust and maintainable solution.

## How did you approach the problem?

- Thorough analysis of the requirements and API structure  
- Definition of core components for folder and document management  
- Implementation of basic CRUD operations for folders and documents  
- Ensuring adherence to REST principles for a clean API  
- Use of factory methods for folder creation  
- Introduction of validation logic to maintain data integrity  
- Implementation of exception handling for user-friendly error messages  

## What was the most difficult part & how did you solve it?

- **Folder and Document Creation**:  
  - The biggest challenge was handling edge cases and validations (e.g., preventing duplicate folder names at the same level)  
  - Solution: Implemented business logic for name validation during folder creation  
  - **Documents with the same name**:  
  - Challenge: Ensuring no duplicate documents are stored  
  - Solution: Appended a counter to the filename when a name duplication is detected  

## What would you have done differently/added if this feature would be shipped into production?

1. **Prevent folders without names**  
   - Ensure that folders can only be created with names  
   - Improve usability and API consistency  
   
2. **Access Control**  
   - Implement detailed authentication and authorization logic  
   - Integrate sessions or JWT to restrict access to authorized users  

3. **Prevent Duplicate Documents**  
   - Ensure that documents with the same name and content cannot be uploaded multiple times  
   - Avoid unnecessary database queries and operations  
   - Improve efficiency and performance, especially with large datasets  