CREATE TABLE Reco (
    QuestionsQuery varchar(5000),
    QuestionsID varchar(5000),
    QuestionsTitle varchar(5000),
    QuestionsBody varchar(5000),
    AnswersBody varchar(5000),
    Similarity float,
);

CREATE TABLE ProfessionalsWF (
    QuestionsQuery varchar(5000),
    ProfessionalsID varchar(5000)
);