from sqlalchemy import func
from models import Transaction


def calculate_ranking(db):

    users = (
        db.query(
            Transaction.user_id,
            func.sum(Transaction.amount),
            func.count(Transaction.id)
        )
        .group_by(Transaction.user_id)
        .all()
    )

    result = []

    for user_id, total, count in users:

        bonus = min(count * 5, 100)

        score = (
            total * 0.7
            + count * 20
            + bonus
        )

        result.append({
            "userId": user_id,
            "score": round(score, 2),
            "totalAmount": total,
            "transactionCount": count
        })

    result.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return result