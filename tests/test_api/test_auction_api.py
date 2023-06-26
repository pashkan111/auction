def test_create_bid(test_client, user, auction):
    # TODO Connects to main db!
    data = dict(
        amount=99,
        user_username=user.username,
        auction_id=auction.id
    )
    response = test_client.post("/bids/", json=data)
    # assert response.status_code == 201
    assert response.json() == {}
